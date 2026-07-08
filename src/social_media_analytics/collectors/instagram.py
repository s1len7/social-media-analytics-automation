import logging
import time
from social_media_analytics.clients.apify import run_apify_actor

logger = logging.getLogger("social-media-analytics")

ACTOR_ID = "apify~instagram-scraper"

def collect_instagram_posts(account_name):
    start_time = time.perf_counter()

    logger.info(f"Instagram collection started: {account_name}")

    payload = {
        "directUrls": [
            f"https://www.instagram.com/{account_name}/"
        ],
        "resultsLimit": 100
    }

    raw_items = run_apify_actor(ACTOR_ID, payload)

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
                "media_count": item.get("childPostsCount"),
                "likes": item.get("likesCount"),
                "comments": item.get("commentsCount"),
                "views": item.get("videoViewCount"),
                "video_duration": item.get("videoDuration"),
                "hashtags": item.get("hashtags"),
                "mentions": item.get("mentions"),
                "location": item.get("locationName"),
                "owner_username": item.get("ownerUsername"),
                "owner_id": item.get("ownerId"),
                "display_url": item.get("displayUrl"),
                "raw_data": item
            }
        )

    elapsed = time.perf_counter() - start_time

    logger.info(f"Instagram collection completed: {account_name}, count={len(posts)}, time={elapsed:.2f}s")

    return posts