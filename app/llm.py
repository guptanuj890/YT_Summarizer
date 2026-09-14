import os
from dotenv import load_dotenv
from openai import OpenAI 
from schema import LessonDraft, ChunkSummary

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcipt_text: str)-> str:
    
    instructions = """
    You are an expert teacher.
    You job is to transform a YouTube transcript into a complete educational lesson.
    
    Cover the important concepts taught in the transcript, explain concepts in simple language, preserve important technical details, include examples mentioned by the instructor.
    Do not invent information that is not supported by the transcript.
    
    Write the lesson as if you are teaching someone who has not watched the video.
    """
    
    response = client.responses.parse(
        model = "gpt-4o",
        instructions = instructions,
        input = transcipt_text,
        text_format = LessonDraft
    )
    
    return response.output_parsed

def summarize_chunk(chunk: str)-> str:
    instructions = """
        You are extracting educational information from one section of a YouTube transcript.
        Summarize this section for another AI that will later combine it with summaries from other sections.
        Preserve important timestamp references.
        The transcript contains timestamps in this format:
        [123.4s] text
        For every important concept or explanation, identify the timestamp where it was taught.
        Do not invent timestamps.
        
        Extract:
        - Concepts taught
        - Important explanations
        - Examples
        - Technical details
        - Important conclusions
        
        Preserve the meaning of the instructor.
        Do not invent insformation.
        Keep the summary concise but information-dense.
    """
    response = client.responses.parse(
        model = "gpt-4o-mini",
        instructions = instructions,
        input = chunk,
        text_format = ChunkSummary
    )
    
    return response.output_parsed


def synthesize_lesson(chunk_summaries: list[str])->LessonDraft:
    input_text = "\n\n".join(
        f"""
        SUMMARY:
        {summary.summary}
        
        SOURCES:
        {summary.sources}
        """
        for summary in chunk_summaries
    )
    
    instructions = """
        You are an expert teacher.
        The input contains summaries of different sections of a YouTube video.
        Create one coherent educational lesson from them.
        
        Important rules:
        1. Cover all the important concepts from the summaries.
        2. Organize related concepts logically.
        3. Preserve source timestamps for cocepts and examples.
        4. Only use timestamps that appear in the provided summaries.
        5. Never invent or modify timestamps.
        6. Use the most relevant timestamp(s) for each concept.
        
        Cover the important concepts taught in the transcript, explain concepts in simple language, preserve important technical details, include examples mentioned by the instructor.
        Do not invent information that is not supported by the transcript.
    """
    
    response = client.responses.parse(
        model = "gpt-4o",
        instructions = instructions,
        input = input_text,
        text_format = LessonDraft
    )
    return response.output_parsed
        