import os
from dotenv import load_dotenv
from openai import OpenAI 
from schema import LessonDraft, ChunkSummary

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcript_text: str, difficulty: str, include_examples: bool, include_quiz: bool) -> LessonDraft:
    
    examples_instruction = (
        "Extract important examples, case studies, and demonstrations."
        if include_examples
        else
        "Ignore examples and demonstrations."
    )

    quiz_instruction = (
        "Identify facts and concepts that could later be turned into quiz questions."
        if include_quiz
        else
        "Do not focus on quiz-worthy content."
    )
    
    instructions = f"""
    Create a complete structured lesson from the transcript.

    The requested difficulty level is: {difficulty}

    Adapt the lesson to this difficulty:

    Beginner:
    - Explain concepts in simple language.
    - Assume little prior knowledge.
    - Explain technical terms when introduced.

    Intermediate:
    - Assume basic knowledge.
    - Use appropriate technical terminology.
    - Provide moderate detail.

    Advanced:
    - Assume strong technical knowledge.
    - Explain deeper technical details.
    - Discuss important nuances, assumptions, and tradeoffs.

    {examples_instruction}

    {quiz_instruction}

    Preserve important source timestamps.
    Do not invent timestamps.
    """

    response = client.responses.parse(
        model="gpt-4o",
        instructions=instructions,
        input=transcript_text,
        text_format=LessonDraft,
    )

    return response.output_parsed

def summarize_chunk(chunk: str, difficulty: str, include_examples: bool, include_quiz: bool) -> ChunkSummary:

    examples_instruction = (
        "Extract important examples, case studies, and demonstrations."
        if include_examples
        else
        "Ignore examples and demonstrations."
    )

    quiz_instruction = (
        "Identify facts and concepts that could later be turned into quiz questions."
        if include_quiz
        else
        "Do not focus on quiz-worthy content."
    )
    
    
    instructions = f"""
    Summarize the important concepts taught in this transcript chunk.

    Difficulty level: {difficulty}

    Beginner:
    - Use simple language.
    - Explain technical terms.

    Intermediate:
    - Use moderate technical depth.

    Advanced:
    - Preserve technical details.
    - Include nuances and tradeoffs.

    {examples_instruction}

    {quiz_instruction}

    Preserve important timestamps.

    Do not invent timestamps.
    """

    response = client.responses.parse(
        model="gpt-4o-mini",
        instructions=instructions,
        input=chunk,
        text_format=ChunkSummary,
    )

    return response.output_parsed

def format_chunk_summaries(chunk_summaries):
    return "\n\n".join(
        f"""
        SUMMARY {i + 1}

        {summary.summary}

        SOURCES:
        {chr(10).join(
            f"- [{source.timestamp:.1f}s] {source.description}"
            for source in summary.sources
        )}
        """
        for i, summary in enumerate(chunk_summaries)
    )

def synthesize_lesson(chunk_summaries: list[str], difficulty: str, include_examples: bool, include_quiz: bool)->LessonDraft:
    input_text = "\n\n".join(
        f"""
        SUMMARY:
        {summary.summary}
        
        SOURCES:
        {summary.sources}
        """
        for summary in chunk_summaries
    )
    
    examples_instruction = (
        "Extract important examples, case studies, and demonstrations."
        if include_examples
        else
        "Ignore examples and demonstrations."
    )

    quiz_instruction = (
        "Identify facts and concepts that could later be turned into quiz questions."
        if include_quiz
        else
        "Do not focus on quiz-worthy content."
    )
    
    instructions = f"""
    Create a complete structured lesson from the provided chunk summaries.

    Difficulty level: {difficulty}

    Adapt the lesson to this difficulty:

    Beginner:
    - Use simple language.
    - Assume little prior knowledge.
    - Explain technical terms.

    Intermediate:
    - Assume basic knowledge.
    - Use appropriate technical terminology.

    Advanced:
    - Assume strong technical knowledge.
    - Include deeper technical details, nuances, and tradeoffs.

    {examples_instruction}

    {quiz_instruction}

    Combine the chunk summaries into one coherent lesson.

    Preserve the important source timestamps.
    Do not invent timestamps.

    Only use information supported by the chunk summaries.
    """
    
    response = client.responses.parse(
        model = "gpt-4o",
        instructions = instructions,
        input = input_text,
        text_format = LessonDraft
    )
    return response.output_parsed
        