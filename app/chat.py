from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def answer_doubt(question: str, lesson, difficulty: str, chat_history: list)-> str:
    concepts_text = "\n\n".join(
        f"Concept: {concept.name}\n"
        f"Explanation: {concept.explanation}"
        for concept in lesson.concepts
    )

    history_text = "\n".join(
        f"{message['role'].upper()}: {message['content']}"
        for message in chat_history
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

Previous conversation:
{history_text}

Student's question:
{question}

Answer the student's question using the lesson content as the
primary source.

Teaching rules:
- Explain clearly at the requested difficulty level.
- Start with intuition before technical details.
- Use a simple example when it helps.
- Connect the answer to concepts from this lesson when relevant.
- Do not invent information that is not supported by the lesson.
- If the question cannot be answered from the lesson, clearly say
  that the lesson does not provide enough information.
- Do not unnecessarily repeat the entire lesson.
"""
    response = client.responses.create(
        model="gpt-4o",
        instructions = prompt,
        input = question,
    )
    
    return response.output_text