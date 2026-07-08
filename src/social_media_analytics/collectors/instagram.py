import logging
import time
from social_media_analytics.clients.apify import run_apify_actor

logger = logging.getLogger("social-media-analytics")

ACTOR_ID = "apify~instagram-scraper"


def collect_instagram_posts(account_name):
    start_time = time.perf_counter()
    logger.info(f"Instagram collection started: {account_name}")

    payload = {
        "directUrls": [f"https://www.instagram.com/{account_name}/"],
        "resultsLimit": 100,
    }

    raw_items = run_apify_actor(ACTOR_ID, payload)

    process_start = time.perf_counter()

    posts = []

    for item in raw_items:
        posts.append(
            {
                "platform": "instagram",
                "account": account_name,
                "id": item.get("id"),
                "shortcode": item.get("shortCode"),
                "timestamp": item.get("timestamp"),
                "url": item.get("url"),
                "caption": item.get("caption"),
                "type": item.get("type"),
                "likes": item.get("likesCount"),
                "comments": item.get("commentsCount"),
                "views": item.get("videoViewCount"),
                "hashtags": item.get("hashtags"),
                "mentions": item.get("mentions"),
                "location": item.get("locationName"),
                "owner_username": item.get("ownerUsername"),
                "owner_id": item.get("ownerId"),
                "display_url": item.get("displayUrl"),
                "raw_data": item,
            }
        )

    process_elapsed = time.perf_counter() - process_start
    total_elapsed = time.perf_counter() - start_time

    logger.info(f"Instagram processing completed: {process_elapsed:.4f}s")
    logger.info(
        f"Instagram collection completed: {account_name}, count={len(posts)}, time={total_elapsed:.2f}s"
    )

    return posts
