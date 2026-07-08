from googleapiclient.discovery import build


def collect_youtube_videos(api_key, channel_id):

    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key
    )

    response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=50
    ).execute()

    videos = []

    for item in response.get("items", []):

        if item["id"]["kind"] != "youtube#video":
            continue

        videos.append(
            {
                "platform": "youtube",
                "channel": channel_id,
                "video_id": item["id"]["videoId"],
                "timestamp": item["snippet"]["publishedAt"],
                "url": (f"https://www.youtube.com/watch?v={item['id']['videoId']}"),
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"]
            }
        )

    return videos