from typing import TypedDict, Annotated
import operator
from schema import LessonDraft, ChunkSummary

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
        list[ChunkSummary],
        operator.add
    ]
    
    difficulty: str
    include_examples: bool
    include_quiz: bool
    video_type: str
    chunk_errors: Annotated[list[str], operator.add]
    
class ChunkState(TypedDict):
    chunk: str
    difficulty: str
    include_examples: bool
    include_quiz: bool
    chunk_errors: list[str]