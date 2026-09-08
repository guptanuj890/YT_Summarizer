from typing import TypedDict, Annotated
import operator
from schema import LessonDraft

class LessonState(TypedDict):
    video_url: str
    video_id: str
    raw_transcript: list[dict]
    transcript_text: str
    token_count: int
    strategy: str
    error: str | None
    lesson_draft: LessonDraft | None
    chunks: list[str]
    chunk_summaries: Annotated[
        list[str],
        operator.add
    ]
    final_lesson_md: str
    
class ChunkState(TypedDict):
    chunk: str