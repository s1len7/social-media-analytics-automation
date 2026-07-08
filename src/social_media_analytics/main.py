import logging
import time
from pathlib import Path

from social_media_analytics.utils.logger import setup_logger

from social_media_analytics.utils.config import load_config

from social_media_analytics.analytics.loader import load_csv_files
from social_media_analytics.analytics.loader import normalize_timestamp
from social_media_analytics.collectors.instagram import collect_instagram_posts
from social_media_analytics.collectors.youtube import collect_youtube_videos
from social_media_analytics.storage.csv_writer import save_csv
from social_media_analytics.reports.summary import create_summary
from social_media_analytics.reports.charts import save_monthly_chart
from social_media_analytics.reports.charts import save_weekly_chart
from social_media_analytics.reports.charts import save_yearly_chart
from social_media_analytics.reports.excel import save_excel

from social_media_analytics.notification.email import create_mail_summary
from social_media_analytics.notification.email import send_email

from social_media_analytics.utils.state import save_state
from social_media_analytics.utils.state import should_run

logger = logging.getLogger("social-media-analytics")


def main():
    start_time = time.perf_counter()

    config = load_config()
    logger = setup_logger(config["logging"]["level"])

    # output_raw = Path(config["output"]["raw_path"])
    # output_processed = Path(config["output"]["processed_path"])
    output_data = Path(config["output"]["data_path"])
    output_data.mkdir(
        parents=True,
        exist_ok=True,
    )

    state_file = output_data / "state" / "state.json"

    if not should_run(state_file):
        logger.info("Monthly report already sent. Skip.")
        return

    logger.info("Social media analytics started")

    instagram_posts = []

    for account in config["instagram"]["accounts"]:
        try:
            posts = collect_instagram_posts(account)
            instagram_posts.extend(posts)
        except Exception:
            logger.exception(f"Instagram collection failed: {account}")

    if instagram_posts:
        save_start = time.perf_counter()
        save_csv(instagram_posts, output_data / "instagram_posts.csv")
        save_elapsed = time.perf_counter() - save_start
        logger.info(
            f"Instagram saved: {len(instagram_posts)}, save_time={save_elapsed:.4f}s"
        )

    youtube_videos = []

    for handle in config["youtube"]["handles"]:
        try:
            videos = collect_youtube_videos(handle)
            youtube_videos.extend(videos)
        except Exception:
            logger.exception(f"YouTube collection failed: {handle}")

    if youtube_videos:
        save_start = time.perf_counter()
        save_csv(youtube_videos, output_data / "youtube_videos.csv")
        save_elapsed = time.perf_counter() - save_start
        logger.info(
            f"YouTube saved: {len(youtube_videos)}, save_time={save_elapsed:.4f}s"
        )

    analysis_start = time.perf_counter()

    analytics_data = load_csv_files(output_data)
    analytics_data = normalize_timestamp(analytics_data)

    platform_counts = analytics_data["platform"].value_counts().to_dict()
    logger.info(f"Platform counts: {platform_counts}")

    save_csv(analytics_data, output_data / "analytics_data.csv")

    summary = create_summary(analytics_data)
    # logger.info(f"Monthly summary:\n{summary['monthly']}")

    report_path = output_data / "social_media_report.xlsx"
    save_excel(summary, report_path)

    chart_path = output_data / "charts"
    chart_path.mkdir(parents=True, exist_ok=True)

    save_yearly_chart(summary["yearly"], chart_path / "yearly.png")
    save_monthly_chart(summary["monthly"], chart_path / "monthly.png")
    save_weekly_chart(summary["weekly"], chart_path / "weekly.png")

    analysis_elapsed = time.perf_counter() - analysis_start
    logger.info(
        f"Analytics completed: rows={len(analytics_data)}, time={analysis_elapsed:.2f}s"
    )

    mail_subject, mail_body = create_mail_summary(summary)

    email_start = time.perf_counter()

    try:
        send_email(
            config=config["mail"],
            subject=mail_subject,
            body=mail_body,
            attachments=[
                report_path,
                # output_raw / "instagram_posts.csv",
                # output_raw / "youtube_videos.csv",
            ],
        )
        email_elapsed = time.perf_counter() - email_start
        logger.info(f"Email completed: time={email_elapsed:.2f}s")
        save_state(state_file)
        logger.info("State saved")
    except Exception:
        logger.exception("Email sending failed")

    elapsed = time.perf_counter() - start_time
    logger.info(f"Completed. Total elapsed={elapsed:.2f}s")


if __name__ == "__main__":
    main()
