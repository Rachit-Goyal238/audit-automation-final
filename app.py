import streamlit as st
import tempfile
import os
import zipfile
import json
import fitz  # PyMuPDF is used for PDF compression
from engines.tata.tata_main import generate_report

from email_module.ui import upload as email_config
from email_module.ui import preview as email_preview
from email_module.ui import draft as email_draft
from email_module.auth.gmail_auth import GmailAuthenticator

st.set_page_config(
    page_title="Audit Report Generator & Dispatcher",
    layout="wide"  # Changed from "centered" to "wide" to prevent horizontal scrolling
)

# --- PDF COMPRESSION HELPER ---
def compress_pdf(file_path: str, max_size_mb: int = 10) -> str:
    """
    Compresses the PDF using PyMuPDF if it exceeds the maximum size limit.
    """
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    
    if file_size_mb <= max_size_mb:
        return file_path
        
    compressed_path = file_path.replace(".pdf", "_compressed.pdf")
    
    try:
        doc = fitz.open(file_path)
        # garbage=4: Remove all unused objects/streams
        # deflate=True: Compress streams
        # clean=True: Clean and sanitize content streams
        doc.save(
            compressed_path, 
            garbage=4, 
            deflate=True, 
            clean=True
        )
        doc.close()
        
        # Verify new size (optional, but good for logging)
        new_size_mb = os.path.getsize(compressed_path) / (1024 * 1024)
        print(f"Compressed PDF from {file_size_mb:.2f}MB to {new_size_mb:.2f}MB")
        
        return compressed_path
    except Exception as e:
        print(f"PDF Compression failed: {e}")
        return file_path
# ------------------------------

st.title("Audit Report Generator")

authenticator = GmailAuthenticator()
credentials = authenticator.authenticate()

with st.sidebar:
    st.header("Authentication")
    if credentials:
        st.success("✅ Signed in to Google")
        if st.button("Sign Out"):
            if "google_credentials" in st.session_state:
                del st.session_state["google_credentials"]
            st.rerun()
    else:
        st.warning("Not signed in to Google")
        st.info("Sign in to generate email drafts.")
        
        oauth_url = os.getenv("OAUTH_URL", "http://localhost:5000")
        
        st.link_button(
            "Sign in with Google", 
            f"{oauth_url}/login", 
            type="primary", 
            use_container_width=True
        )

if "downloads" not in st.session_state:
    st.session_state.downloads = None

if "email_data" not in st.session_state:
    st.session_state.email_data = {
        "result": None,
        "subject": "",
        "to": "",
        "cc": "",
        "filename": None,
        "file_bytes": None,
        "attachments": []
    }

tab_generate, tab_email = st.tabs(["1. Generate Report", "2. Dispatch Email"])

with tab_generate:
    audit_id = st.text_input("Enter Audit ID")
    master_file = st.file_uploader("Upload Master Excel", type=["xlsx"])

    with open("templates.json", "r", encoding="utf-8") as f:
        template_repository = json.load(f)

    client = st.selectbox("Select Client", ["TATA Capital", "YesBank"])

    if client == "YesBank":
        st.link_button(
            "Open YesBank Report Generator",
            "https://audit-report-generator-yesbank.streamlit.app/",
            use_container_width=True
        )
        st.stop()

    template_type = st.selectbox(
        "Select Template", 
        list(template_repository["TATA Capital"].keys())
    )

    report_pdf = st.file_uploader("Upload Audit Report PDF", type=["pdf"])
    annexure_pdf = st.file_uploader("Upload Annexure PDF", type=["pdf"])

    if st.button("Generate Report"):
        if not audit_id:
            st.error("Please enter Audit ID")
        elif not all([master_file, report_pdf]):
            st.error("Please upload all files")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    master_path = os.path.join(temp_dir, master_file.name)
                    with open(master_path, "wb") as f:
                        f.write(master_file.getbuffer())

                    report_path = os.path.join(temp_dir, report_pdf.name)
                    with open(report_path, "wb") as f:
                        f.write(report_pdf.getbuffer())

                    annexure_path = None
                    if annexure_pdf:
                        annexure_path = os.path.join(temp_dir, annexure_pdf.name)
                        with open(annexure_path, "wb") as f:
                            f.write(annexure_pdf.getbuffer())

                    with st.spinner("Generating report..."):
                        result = generate_report(
                            audit_id, master_path, client, template_type, report_path, annexure_path
                        )

                    # --- COMPRESS THE FINAL PDF BEFORE PACKAGING ---
                    with st.spinner("Compressing final report for email limits..."):
                        result["final"] = compress_pdf(result["final"], max_size_mb=10)
                    # -----------------------------------------------

                    zip_file = os.path.join(tempfile.gettempdir(), "Audit_Report_Package.zip")
                    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
                        for file_path in [result["excel"], result["pdf"], result["evidence"], result["final"]]:
                            zipf.write(file_path, arcname=os.path.basename(file_path))

                    with open(zip_file, "rb") as f:
                        zip_bytes = f.read()
                    with open(result["excel"], "rb") as f:
                        excel_bytes = f.read()
                    with open(result["evidence"], "rb") as f:
                        evidence_bytes = f.read()
                    with open(result["final"], "rb") as f:
                        final_bytes = f.read()

                    st.session_state.downloads = {
                        "zip": zip_bytes,
                        "excel": excel_bytes,
                        "evidence": evidence_bytes,
                        "final": final_bytes,
                        "excel_name": os.path.basename(result["excel"]),
                        "evidence_name": os.path.basename(result["evidence"]),
                        "final_name": os.path.basename(result["final"])
                    }

            except Exception as e:
                st.error(str(e))

    if st.session_state.downloads:
        downloads = st.session_state.downloads
        st.success("Report generated successfully. Proceed to the 'Dispatch Email' tab.")

        st.download_button(
            label="Download Complete Package (ZIP)",
            data=downloads["zip"],
            file_name="Audit_Report_Package.zip",
            mime="application/zip"
        )
        st.subheader("Individual Downloads")
        st.download_button(
            "Download Excel Report",
            data=downloads["excel"],
            file_name=downloads["excel_name"],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.download_button(
            "Download Final Report",
            data=downloads["final"],
            file_name=downloads["final_name"],
            mime="application/pdf"
        )

with tab_email:
    email_config.render()
    
    st.divider()
    st.subheader("Email Preview")
    email_preview.render()
    
    st.divider()
    email_draft.render()