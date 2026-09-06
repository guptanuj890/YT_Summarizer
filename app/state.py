from typing import TypedDict

class LessonState(TypedDict):
    video_url: str
    video_id: str
    raw_transcript: list[dict]
    transcript_text: str
    token_count: int
    strategy: str
    error: str | None
    lesson_draft: str
    chunks: list[str]