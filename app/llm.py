import os
from dotenv import load_dotenv
from openai import OpenAI 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_lesson(transcipt_text: str)-> str:
    
    instructions = """
    You are an expert teacher.
    You job is to transform a YouTube transcript into a clear, structured lesson.
    
    Requirements:
    -Cover the important concepts taught in the transcript.
    -Explain concepts in simple language.
    -Preserve important technical details.
    -Include examples mentioned by the instructor.
    -Do not invent information that is not supported by the transcript.
    -Organize the lesson with clear Markdown headings.
    -End with a concise summary.
    
    Write the lesson as if you are teaching someone who has not watched the video.
    """
    
    response = client.responses.create(
        model = "gpt-4o",
        instructions = instructions,
        input = transcipt_text,
    )
    
    return response.output_text