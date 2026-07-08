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

    video_ids = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    logger.info(f"YouTube video ids collected: {len(video_ids)}")

    videos = []
    detail_start = time.perf_counter()

    for index in range(0, len(video_ids), 50):
        batch_ids = video_ids[index:index + 50]

        response = youtube.videos().list(
            part="snippet,statistics,contentDetails,status,topicDetails,recordingDetails,liveStreamingDetails",
            id=",".join(batch_ids)
        ).execute()

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            content_details = item.get("contentDetails", {})
            status = item.get("status", {})
            topic_details = item.get("topicDetails", {})
            recording_details = item.get("recordingDetails", {})
            live_details = item.get("liveStreamingDetails", {})

            videos.append({
                "platform": "youtube",
                "channel_id": item.get("snippet", {}).get("channelId"),
                "channel_title": snippet.get("channelTitle"),
                "video_id": item.get("id"),
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "published_at": snippet.get("publishedAt"),
                "category_id": snippet.get("categoryId"),
                "tags": snippet.get("tags"),
                "thumbnail_default": snippet.get("thumbnails", {}).get("default", {}).get("url"),
                "thumbnail_medium": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                "thumbnail_high": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                "default_language": snippet.get("defaultLanguage"),
                "default_audio_language": snippet.get("defaultAudioLanguage"),
                "view_count": statistics.get("viewCount"),
                "like_count": statistics.get("likeCount"),
                "comment_count": statistics.get("commentCount"),
                "favorite_count": statistics.get("favoriteCount"),
                "duration": content_details.get("duration"),
                "dimension": content_details.get("dimension"),
                "definition": content_details.get("definition"),
                "caption": content_details.get("caption"),
                "licensed_content": content_details.get("licensedContent"),
                "projection": content_details.get("projection"),
                "upload_status": status.get("uploadStatus"),
                "privacy_status": status.get("privacyStatus"),
                "license": status.get("license"),
                "embeddable": status.get("embeddable"),
                "public_stats_viewable": status.get("publicStatsViewable"),
                "made_for_kids": status.get("madeForKids"),
                "topic_categories": topic_details.get("topicCategories"),
                "recording_date": recording_details.get("recordingDate"),
                "location": recording_details.get("location"),
                "scheduled_start_time": live_details.get("scheduledStartTime"),
                "actual_start_time": live_details.get("actualStartTime"),
                "actual_end_time": live_details.get("actualEndTime"),
                "concurrent_viewers": live_details.get("concurrentViewers"),
                "url": f"https://www.youtube.com/watch?v={item.get('id')}",
                "raw_data": item
            })

    detail_elapsed = time.perf_counter() - detail_start
    logger.info(f"YouTube video details collected: {detail_elapsed:.2f}s")

    elapsed = time.perf_counter() - start_time
    logger.info(f"YouTube collection completed: {channel_handle}, count={len(videos)}, time={elapsed:.2f}s")

    return videos