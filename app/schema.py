from pydantic import BaseModel


class SourceReference(BaseModel):
    timestamp: float
    description: str
    
class Concept(BaseModel):
    name: str
    explanation: str
    sources: list[SourceReference]
    analogy: str | None = None
    
class Example(BaseModel):
    description: str
    sources: list[SourceReference]
    
class QuizQuestion(BaseModel):
    question: str
    answer: str
    
class LessonDraft(BaseModel):
    title: str
    concepts: list[Concept]
    examples: list[Example]
    summary: str
    quiz: list[QuizQuestion]
    key_takeaways: list[str]
    follow_up_questions: list[str]
    

class ChunkSummary(BaseModel):
    summary: str
    sources: list[SourceReference]