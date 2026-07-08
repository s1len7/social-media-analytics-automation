import time
import logging
from pathlib import Path

from social_media_analytics.utils.config import load_config
from social_media_analytics.utils.logger import setup_logger
from social_media_analytics.collectors.instagram import collect_instagram_posts
from social_media_analytics.storage.csv_writer import save_csv
from social_media_analytics.storage.json_writer import save_json

def main():
    start_time = time.perf_counter()
    config = load_config()
    logger = setup_logger(config["logging"]["level"])
    logger.info("Social media analytics started")
    output_raw = Path(config["output"]["raw_path"])
    output_csv = Path(config["output"]["csv_path"])
    instagram_posts = []

    for account in config["instagram"]["accounts"]:
        try:
            posts = collect_instagram_posts(account)
            instagram_posts.extend(posts)
        except Exception:
            logger.exception(f"Instagram collection failed: {account}")

    if instagram_posts:
        save_start = time.perf_counter()
        save_json(instagram_posts, output_raw / "instagram_raw.json")
        save_csv(instagram_posts, output_csv / "instagram_posts.csv")
        save_elapsed = time.perf_counter() - save_start
        logger.info(f"Instagram saved: {len(instagram_posts)}, save_time={save_elapsed:.4f}s")

    elapsed = time.perf_counter() - start_time
    logger.info(f"Completed. Total elapsed={elapsed:.2f}s")

if __name__ == "__main__":
    main()