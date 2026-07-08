import os
import time
import requests
import logging

logger = logging.getLogger("social-media-analytics")

def run_apify_actor(actor_id, payload):
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise ValueError("APIFY_API_TOKEN is missing")

    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items"
    logger.info(f"Apify request started: {actor_id}")

    start_time = time.perf_counter()

    response = requests.post(url, params={"token": token}, json=payload, timeout=300)

    elapsed = time.perf_counter() - start_time

    logger.info(f"Apify API completed: {elapsed:.2f}s")

    response.raise_for_status()

    data = response.json()

    logger.info(f"Apify items received: {len(data)}")

    return data