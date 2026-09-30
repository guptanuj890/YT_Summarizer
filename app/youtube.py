import re
from urllib.parse import urlparse, parse_qs


VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


def validate_video_id(video_id: str) -> str:
    if not VIDEO_ID_PATTERN.fullmatch(video_id):
        raise ValueError("Invalid YouTube video ID")

    return video_id


def extract_video_id(url: str) -> str:
    parsed = urlparse(url.strip())

    hostname = (parsed.hostname or "").lower()
    path = parsed.path.strip("/")

    video_id = None

    # youtube.com / www.youtube.com / m.youtube.com
    if hostname in {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
    }:

        # /watch?v=VIDEO_ID
        if path == "watch":
            video_ids = parse_qs(parsed.query).get("v")

            if video_ids:
                video_id = video_ids[0]

        # /shorts/VIDEO_ID
        elif path.startswith("shorts/"):
            parts = path.split("/")

            if len(parts) >= 2:
                video_id = parts[1]

        # /embed/VIDEO_ID
        elif path.startswith("embed/"):
            parts = path.split("/")

            if len(parts) >= 2:
                video_id = parts[1]

        # /live/VIDEO_ID
        elif path.startswith("live/"):
            parts = path.split("/")

            if len(parts) >= 2:
                video_id = parts[1]

    # youtu.be/VIDEO_ID
    elif hostname == "youtu.be":
        if path:
            video_id = path.split("/")[0]

    if not video_id:
        raise ValueError(
            "Invalid or unsupported YouTube URL"
        )

    return validate_video_id(video_id)