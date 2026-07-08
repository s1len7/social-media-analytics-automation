import os
import time
import logging
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

logger = logging.getLogger("social-media-analytics")

def get_youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY is missing")
    return build("youtube", "v3", developerKey=api_key)

def resolve_channel_id(youtube, channel_handle):
    start_time = time.perf_counter()
    handle = channel_handle.replace("@", "")
    logger.info(f"YouTube channel lookup started: @{handle}")

    response = youtube.channels().list(
        part="id,snippet,contentDetails",
        forHandle=handle
    ).execute()

    if not response.get("items"):
        raise ValueError(f"YouTube channel not found: @{handle}")

    channel = response["items"][0]
    channel_id = channel["id"]

    elapsed = time.perf_counter() - start_time
    logger.info(f"YouTube channel resolved: @{handle} -> {channel_id}, time={elapsed:.2f}s")

    return channel_id

def collect_youtube_videos(channel_handle):
    start_time = time.perf_counter()
    youtube = get_youtube_client()

    channel_id = resolve_channel_id(youtube, channel_handle)

    logger.info(f"YouTube collection started: {channel_id}")

    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            videos.append({
                "platform": "youtube",
                "channel_id": channel_id,
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_at": item["snippet"]["publishedAt"],
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "raw_data": item
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    logger.info(f"YouTube metadata collected: {len(videos)}")

    statistic_start = time.perf_counter()

    video_ids = [video["video_id"] for video in videos]
    statistics = {}

    for index in range(0, len(video_ids), 50):
        batch_ids = video_ids[index:index + 50]

        response = youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(batch_ids)
        ).execute()

        for item in response.get("items", []):
            statistics[item["id"]] = {
                "view_count": item["statistics"].get("viewCount"),
                "like_count": item["statistics"].get("likeCount"),
                "comment_count": item["statistics"].get("commentCount"),
                "duration": item["contentDetails"].get("duration")
            }

    statistic_elapsed = time.perf_counter() - statistic_start
    logger.info(f"YouTube statistics collected: {statistic_elapsed:.2f}s")

    for video in videos:
        video.update(
            statistics.get(video["video_id"], {})
        )

    elapsed = time.perf_counter() - start_time
    logger.info(f"YouTube collection completed: {channel_handle}, count={len(videos)}, time={elapsed:.2f}s")

    return videos