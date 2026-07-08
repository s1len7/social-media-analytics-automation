import logging
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

import markdown
from dotenv import load_dotenv
from jinja2 import Template

logger = logging.getLogger("social-media-analytics")

load_dotenv()


def create_mail_summary(summary):
    template_path = Path(__file__).parent / "templates" / "monthly_report.md"
    template = Template(template_path.read_text(encoding="utf-8"))

    monthly = summary["monthly"].copy()
    monthly["month"] = monthly["month"].astype(str)

    today = datetime.today()

    if today.month == 1:
        report_year = today.year - 1
        report_month = 12
    else:
        report_year = today.year
        report_month = today.month - 1

    report_month_str = f"{report_year}-{report_month:02d}"

    target = monthly.loc[
        monthly["month"] == report_month_str
    ]

    if target.empty:
        raise ValueError(
            f"Previous month data not found: {report_month_str}"
        )

    instagram = target.loc[
        target["platform"] == "instagram",
        "count",
    ]

    youtube = target.loc[
        target["platform"] == "youtube",
        "count",
    ]

    instagram_count = int(
        instagram.iloc[0]
    ) if not instagram.empty else 0

    youtube_count = int(
        youtube.iloc[0]
    ) if not youtube.empty else 0

    total_count = (
        instagram_count
        + youtube_count
    )

    body = template.render(
        report_month=report_month_str,
        instagram_count=instagram_count,
        youtube_count=youtube_count,
        total_count=total_count,
    )

    subject = (
        f"[Social Media Analytics] "
        f"{report_month_str} Report"
    )

    return subject, body


def send_email(config, subject, body, attachments):
    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]

    recipients = [
        email.strip()
        for email in os.getenv(
            "MAIL_RECIPIENTS",
            "",
        ).split(",")
        if email.strip()
    ]

    if not recipients:
        raise ValueError("MAIL_RECIPIENTS is missing")

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        raise ValueError("SMTP credentials are missing")

    message = EmailMessage()
    message["Subject"] = subject
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
            logger.warning(f"Attachment skipped: {file_path}")
            continue

        with file_path.open("rb") as file:
            message.add_attachment(
                file.read(),
                maintype="application",
                subtype="octet-stream",
                filename=file_path.name,
            )

        logger.info(f"Attachment added: {file_path.name}")

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