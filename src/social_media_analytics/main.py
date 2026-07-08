import time
from pathlib import Path
import logging

from social_media_analytics.utils import logger
from social_media_analytics.utils.config import load_config
from social_media_analytics.utils.logger import setup_logger

from social_media_analytics.collectors.instagram import collect_instagram_posts
from social_media_analytics.collectors.youtube import collect_youtube_videos

from social_media_analytics.storage.csv_writer import save_csv
from social_media_analytics.storage.json_writer import save_json

from social_media_analytics.analytics.loader import load_csv_files
from social_media_analytics.analytics.loader import normalize_timestamp
from social_media_analytics.reports.summary import create_summary

from social_media_analytics.reports.charts import save_monthly_chart
from social_media_analytics.reports.charts import save_weekly_chart
from social_media_analytics.reports.charts import save_yearly_chart
from social_media_analytics.reports.excel import save_excel

from social_media_analytics.notification.email import send_email

def main():
    start_time = time.perf_counter()
    config = load_config()
    logger = setup_logger(config["logging"]["level"])
    logger.info("Social media analytics started")

    output_raw = Path(config["output"]["raw_path"])
    output_csv = Path(config["output"]["processed_path"])

    instagram_posts = []

    for account in config["instagram"]["accounts"]:
        try:
            posts = collect_instagram_posts(account)
            instagram_posts.extend(posts)
        except Exception:
            logger.exception(f"Instagram collection failed: {account}")

    if instagram_posts:
        save_start = time.perf_counter()
        # save_json(instagram_posts, output_raw / "instagram_raw.json")
        save_csv(instagram_posts, output_raw / "instagram_posts.csv")
        save_elapsed = time.perf_counter() - save_start
        logger.info(f"Instagram saved: {len(instagram_posts)}, save_time={save_elapsed:.4f}s")

    youtube_videos = []

    for handle in config["youtube"]["handles"]:
        try:
            videos = collect_youtube_videos(handle)
            youtube_videos.extend(videos)
        except Exception:
            logger.exception(f"YouTube collection failed: {handle}")

    if youtube_videos:
        save_start = time.perf_counter()
        # save_json(youtube_videos, output_raw / "youtube_raw.json")
        save_csv(youtube_videos, output_raw / "youtube_videos.csv")
        save_elapsed = time.perf_counter() - save_start
        logger.info(f"YouTube saved: {len(youtube_videos)}, save_time={save_elapsed:.4f}s")

    
    analysis_start = time.perf_counter()

    analytics_data = load_csv_files(output_raw)
    analytics_data = normalize_timestamp(analytics_data)
    logger.info(f"Platform counts: {analytics_data['platform'].value_counts().to_dict()}")
    save_csv(analytics_data, output_csv / "analytics_data.csv")

    summary = create_summary(analytics_data)
    save_excel(summary, output_csv / "social_media_report.xlsx")

    chart_path = output_csv / "charts"
    chart_path.mkdir(parents=True, exist_ok=True)

    save_yearly_chart(summary["yearly"], chart_path / "yearly.png")
    save_monthly_chart(summary["monthly"], chart_path / "monthly.png")
    save_weekly_chart(summary["weekly"], chart_path / "weekly.png")

    analysis_elapsed = time.perf_counter() - analysis_start
    logger.info(f"Analytics completed: rows={len(analytics_data)}, time={analysis_elapsed:.2f}s")

    email_start = time.perf_counter()

    send_email(
        subject="[Social Media Analytics] Monthly Report",
        body=(
            "Social media analytics report is completed.\n\n"
            "Attached files:\n"
            "- social_media_report.xlsx\n"
            "- instagram_posts.csv\n"
            "- youtube_videos.csv"
        ),
        attachments=[
            output_csv / "social_media_report.xlsx",
            output_raw / "instagram_posts.csv",
            output_raw / "youtube_videos.csv",
        ],
    )

    email_elapsed = time.perf_counter() - email_start

    logger.info(
        f"Email sent, time={email_elapsed:.2f}s"
    )

    elapsed = time.perf_counter() - start_time
    logger.info(f"Completed. Total elapsed={elapsed:.2f}s")

if __name__ == "__main__":
    main()