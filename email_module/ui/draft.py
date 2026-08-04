import streamlit as st
import streamlit.components.v1 as components
from email_module.services.gmail_service import GmailService
from email_module.utils.session import get

def render():
    email = get()

    disabled = email.get("result") is None

    if st.button(
        "📨 Generate Gmail Draft",
        type="primary",
        use_container_width=True,
        disabled=disabled
    ):
        try:
            credentials = st.session_state.get("google_credentials")

            if credentials is None:
                st.error("Please sign in with Google first.")
                return

            gmail = GmailService(credentials)

            gmail.create_draft(
                to=email.get("to", ""),
                cc=email.get("cc", ""),
                subject=email.get("subject", ""),
                html=email["result"]["html"],
                attachments=email.get("attachments", [])
            )

            st.success("✅ Gmail Draft Created Successfully!")

            components.html(
                """
                <script>
                window.open("https://mail.google.com/mail/u/0/#drafts", "_blank");
                </script>
                """,
                height=0,
            )

        except Exception as e:
            st.exception(e)