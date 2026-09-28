from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

MAX_CHAT_MESSAGES = 12

def answer_doubt(
    question: str,
    lesson,
    difficulty: str,
    chat_history: list,
    chat_summary: str
) -> str:

    concepts_text = "\n\n".join(
        f"Concept: {concept.name}\n"
        f"Explanation: {concept.explanation}"
        for concept in lesson.concepts
    )

    # Keep only the most recent messages
    recent_history = chat_history[-MAX_CHAT_MESSAGES:]

    history_text = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in recent_history
    )

    prompt = f"""
You are a helpful and engaging teacher.

The student is learning from a YouTube lesson.

Difficulty level:
{difficulty}

Lesson title:
{lesson.title}

Lesson concepts:
{concepts_text}

Lesson summary:
{lesson.summary}

Previous conversation summary:
{chat_summary}

Recent conversation:
{history_text}

Student's current question:
{question}

Answer the student's current question using the lesson content as the
primary source.

Teaching rules:
- Answer the student's current question directly.
- Use the previous conversation to understand references such as
  "this", "that", "the previous concept", or "why?"
- Start with intuition before technical details.
- Use examples when they genuinely help.
- Adapt the explanation to the student's difficulty level.
- Connect the answer to the lesson whenever relevant.
- Use Markdown for formatting.
- Use fenced code blocks for code.
- Use LaTeX for mathematical equations.
- Do not unnecessarily repeat information already explained.
- Do not invent information that is unsupported by the lesson.
- If the lesson does not contain enough information to answer,
  clearly say so rather than pretending that it does.
"""

    response = client.responses.create(
        model="gpt-4o",
        instructions=prompt,
        input=question
    )

    return response.output_text

def summarize_chat_history(chat_history: list) -> str:
    if not chat_history:
        return ""
    
    conversation = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in chat_history
    )
    
    response = client.responses.create(
        model = "gpt-4o-mini",
        instructions = """
        
        Summarize this student-teacher conversation.
        
        Preserve:
        - concepts the student asked about
        - explanations already given
        - misunderstandings or areas of confusion
        - examples that were discussed
        - important conclusions
        - terminology introduced
        
        Do not add new information.
        Keep the summary concise and useful for continuing the conversation.
        """,
        input = conversation      
    )
    return response.output_text