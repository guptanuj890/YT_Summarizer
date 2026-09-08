import os
from dotenv import load_dotenv
from openai import OpenAI 
from schema import LessonDraft

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
    response = client.responses.create(
        model = "gpt-4o-mini",
        instructions = instructions,
        input = chunk
    )
    
    return response.output_text


def synthesize_lesson(chunk_summaries: list[str])->LessonDraft:
    combined_summaries = "\n\n".join(
        f"SECTION {i+1}\n{summary}"
        for i, summary in enumerate(chunk_summaries)
    )
    
    instructions = """
        You are an expert teacher.
        The input contains summaries of different sections of a YouTube video.
        Create one coherent educational lesson from them.
        
        Cover the important concepts taught in the transcript, explain concepts in simple language, preserve important technical details, include examples mentioned by the instructor.
        Do not invent information that is not supported by the transcript.
    """
    
    response = client.responses.parse(
        model = "gpt-4o",
        instructions = instructions,
        input = combined_summaries,
        text_format = LessonDraft
    )
    return response.output_text
        