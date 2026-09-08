from pydantic import BaseModel

class Concept(BaseModel):
    name: str
    explanation: str
    
class Example(BaseModel):
    description: str
    
class QuizQuestion(BaseModel):
    question: str
    answer: str
    
class LessonDraft(BaseModel):
    title: str
    concepts: list[Concept]
    examples: list[Example]
    summary: str
    quiz: list[QuizQuestion]