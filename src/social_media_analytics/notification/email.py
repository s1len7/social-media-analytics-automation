import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_email(subject, body, attachments):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    mail_to = os.getenv("MAIL_TO")

    if not all(
        [
            smtp_server,
            smtp_user,
            smtp_password,
            mail_to,
        ]
    ):
        raise ValueError("SMTP configuration is missing")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_user
    message["To"] = mail_to
    message.set_content(body)

    for attachment in attachments:
        file_path = Path(attachment)

        with file_path.open("rb") as file:
            file_data = file.read()

        message.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_path.name,
        )

    with smtplib.SMTP(
        smtp_server,
        smtp_port,
    ) as server:
        server.starttls()
        server.login(
            smtp_user,
            smtp_password,
        )
        server.send_message(message)