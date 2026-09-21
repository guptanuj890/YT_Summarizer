from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
)


def fetch_transcript(video_id: str, languages=None):

    if languages is None:
        languages = ["en"]

    api = YouTubeTranscriptApi()

    try:
        transcript = api.fetch(
            video_id,
            languages=languages
        )

        segments = []

        for segment in transcript:
            segments.append({
                "text": segment.text,
                "start": segment.start,
                "duration": segment.duration
            })

        return segments

    except TranscriptsDisabled:
        raise ValueError(
            "Transcripts are disabled for this video."
        )

    except NoTranscriptFound:
        raise ValueError(
            f"No transcript found for languages: {languages}"
        )

    except Exception as e:
        raise ValueError(
            f"Unable to fetch transcript: {str(e)}"
        ) from e


def transcript_to_text(segments):
    return " ".join(
        segment["text"]
        for segment in segments
    )