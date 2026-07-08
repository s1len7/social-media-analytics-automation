import logging
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

import markdown
from dotenv import load_dotenv
from jinja2 import Template

logger = logging.getLogger("social-media-analytics")

load_dotenv()


def create_mail_summary(summary):
    template_path = (
        Path(__file__).parent
        / "templates"
        / "monthly_report.md"
    )

    template = Template(
        template_path.read_text(
            encoding="utf-8",
        )
    )

    monthly = summary["monthly"]

    latest = monthly.iloc[-1]

    instagram_count = latest.get(
        "instagram_count",
        0,
    )

    youtube_count = latest.get(
        "youtube_count",
        0,
    )

    markdown_body = template.render(
        report_month=str(latest["month"]),
        instagram_count=instagram_count,
        youtube_count=youtube_count,
        total_count=(
            instagram_count
            + youtube_count
        ),
    )

    return markdown_body


def send_email(config, body, attachments):
    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    recipients = [
        email.strip()
        for email in os.getenv("MAIL_RECIPIENTS", "",).split(",")
        if email.strip()
    ]
    if not recipients:
        raise ValueError("MAIL_RECIPIENTS is missing")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        raise ValueError("SMTP credentials are missing")

    message = EmailMessage()

    message["Subject"] = config["subject"]
    message["From"] = smtp_user
    message["To"] = ", ".join(recipients)

    message.set_content(body)

    html_body = markdown.markdown(
        body,
        extensions=[
            "tables",
        ],
    )

    message.add_alternative(
        html_body,
        subtype="html",
    )

    for attachment in attachments:
        file_path = Path(attachment)

        if not file_path.exists():
            logger.warning(
                f"Attachment skipped: {file_path}"
            )
            continue

        with file_path.open("rb") as file:
            file_data = file.read()

        message.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=file_path.name,
        )

        logger.info(
            f"Attachment added: {file_path.name}"
        )

    logger.info(
        f"SMTP connection started: {smtp_server}:{smtp_port}"
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

    logger.info(
        f"Email sent: recipients={recipients}"
    )