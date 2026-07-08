import os
import time
import threading
import requests
import logging

logger = logging.getLogger("social-media-analytics")


def heartbeat(stop_event, interval=10):
    while not stop_event.wait(interval):
        logger.info("Apify request still running...")


def run_apify_actor(actor_id, payload):
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise ValueError("APIFY_API_TOKEN is missing")

    url = f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items"
    logger.info(f"Apify request started: {actor_id}")

    stop_event = threading.Event()
    heartbeat_thread = threading.Thread(
        target=heartbeat, args=(stop_event,), daemon=True
    )
    heartbeat_thread.start()

    start_time = time.perf_counter()

    try:
        response = requests.post(
            url, params={"token": token}, json=payload, timeout=300
        )
    finally:
        stop_event.set()

    api_elapsed = time.perf_counter() - start_time
    logger.info(f"Apify API completed: {api_elapsed:.2f}s")

    response.raise_for_status()

    parse_start = time.perf_counter()
    data = response.json()
    parse_elapsed = time.perf_counter() - parse_start

    logger.info(f"Apify JSON parsed: {parse_elapsed:.4f}s")
    logger.info(f"Apify items received: {len(data)}")

    return data
