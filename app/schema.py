from pydantic import BaseModel


class SourceReference(BaseModel):
    timestamp: float
    description: str
    
class Concept(BaseModel):
    name: str
    explanation: str
    sources: list[SourceReference]
    
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
    

class ChunkSummary(BaseModel):
    summary: str
    sources: list[SourceReference]