import os
import re
import fitz
import pandas as pd
import json
import subprocess

from pypdf import PdfReader, PdfWriter


def extract_pdf_header(pdf_path):

    pdf = fitz.open(pdf_path)

    page = pdf[0]

    text = page.get_text()

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    data = {}

    for i, line in enumerate(lines):

        try:

            if line == "AGENCY NAME":
                data["agency_name"] = lines[i + 1]

            elif line == "OPERATING ADDRESS":

                address_lines = []

                j = i + 1

                while j < len(lines):

                    if lines[j] == "CURRENT EMAIL ID":
                        break

                    address_lines.append(lines[j])

                    j += 1

                data["operating_address"] = " ".join(
                    address_lines
                )

            elif line == "TYPE OF AGENCY":
                data["agency_type"] = lines[i + 1]

            elif line == "COLLECTION MANAGER":
                data["collection_manager"] = lines[i + 1]

            elif line == "AGENCY MANAGER":
                data["agency_manager"] = lines[i + 1]

        except IndexError:
            pass

    pdf.close()

    return data

def extract_evidence_pages(input_pdf, output_pdf):

    pdf = fitz.open(input_pdf)

    evidence_pdf = fitz.open()

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        text = page.get_text()

        if re.search(
            r"Observation\s*#?\s*\d+",
            text,
            re.IGNORECASE
        ):

            evidence_pdf.insert_pdf(
                pdf,
                from_page=page_num,
                to_page=page_num
            )

    evidence_pdf.save(output_pdf)

    evidence_pdf.close()
    pdf.close()

def merge_pdfs(pdf1, pdf2, pdf3, output_pdf):

    writer = PdfWriter()

    for pdf_file in [pdf1, pdf2, pdf3]:

        if not pdf_file:
            continue
        
        reader = PdfReader(pdf_file)

        for page in reader.pages:
            writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

import shutil
import subprocess
import os
import time

def excel_to_pdf(excel_path, pdf_path):
    soffice_path = shutil.which("libreoffice") or shutil.which("soffice")

    if not soffice_path:
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                soffice_path = path
                break

    if not soffice_path:
        raise Exception("LibreOffice not installed")

    output_dir = os.path.dirname(os.path.abspath(pdf_path))
    excel_abs = os.path.abspath(excel_path)
    pdf_abs = os.path.abspath(pdf_path)

    # 1. Dynamically write the PyUNO script to force calculation and scaling
    pyuno_script = os.path.join(output_dir, "pyuno_converter.py")
    with open(pyuno_script, "w") as f:
        f.write("""
import uno
from com.sun.star.beans import PropertyValue
import os
import sys

def convert(input_excel, output_pdf):
    try:
        localContext = uno.getComponentContext()
        resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)
        
        # Connect to the background LibreOffice instance
        ctx = resolver.resolve("uno:socket,host=127.0.0.1,port=2002;urp;StarOffice.ComponentContext")
        desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

        # UpdateDocMode 3 forces LibreOffice to update cross-sheet links and cache
        inProps = (
            PropertyValue("Hidden", 0, True, 0),
            PropertyValue("UpdateDocMode", 0, 3, 0) 
        )
        
        url = uno.systemPathToFileUrl(os.path.abspath(input_excel))
        doc = desktop.loadComponentFromURL(url, "_blank", 0, inProps)

        # Force a full recalculation of all IFS and SUMIF formulas
        doc.calculateAll()

        # Export to PDF preserving the layout
        outProps = (
            PropertyValue("FilterName", 0, "calc_pdf_Export", 0),
        )
        outUrl = uno.systemPathToFileUrl(os.path.abspath(output_pdf))
        doc.storeToURL(outUrl, outProps)
        doc.close(True)
        
    except Exception as e:
        print(f"PyUNO Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
""")

    # 2. Boot LibreOffice in the background listening on port 2002
    lo_process = subprocess.Popen(
        [
            soffice_path, "--headless", "--invisible", "--nocrashreport", 
            "--nodefault", "--nofirststartwizard", "--nologo", "--norestore", 
            "--accept=socket,host=127.0.0.1,port=2002;urp;"
        ]
    )

    try:
        # Give LibreOffice 5 seconds to fully initialize the socket (Render servers can be slow)
        time.sleep(5)

        # 3. Execute using the OS Python (/usr/bin/python3) which contains the 'uno' module
        # We inject the PYTHONPATH so it finds the Debian packages, and capture the exact error output
        env = os.environ.copy()
        env["PYTHONPATH"] = "/usr/lib/python3/dist-packages"
        
        result = subprocess.run(
            ["/usr/bin/python3", pyuno_script, excel_abs, pdf_abs], 
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode != 0:
            # This will now print the EXACT error to your Render logs instead of a generic Exit 1
            raise Exception(f"PyUNO Script Failed!\nError: {result.stderr}\nOutput: {result.stdout}")

    finally:
        # 4. Terminate LibreOffice and delete the temporary script
        lo_process.terminate()
        lo_process.wait()
        if os.path.exists(pyuno_script):
            os.remove(pyuno_script)