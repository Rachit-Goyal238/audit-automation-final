import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


class GmailService:

    def __init__(self, credentials):
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        self.service = build(
            "gmail",
            "v1",
            credentials=credentials
        )

    def create_draft(
        self,
        to="",
        cc="",
        subject="",
        html="",
        attachments=None
    ):

        if attachments is None:
            attachments = []

        message = MIMEMultipart("mixed")

        message["To"] = to
        message["Cc"] = cc
        message["Subject"] = subject

        related = MIMEMultipart("related")
        message.attach(related)

        related.attach(
            MIMEText(html, "html")
        )

        for attachment in attachments:

            part = MIMEApplication(
                attachment["content"]
            )

            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment["filename"]
            )

            message.attach(part)

        raw = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        draft = {
            "message": {
                "raw": raw
            }
        }

        return self.service.users().drafts().create(
            userId="me",
            body=draft
        ).execute()