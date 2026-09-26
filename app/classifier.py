from typesafe_sdk import Choice, TypeSafeClient
from dotenv import load_dotenv

load_dotenv()

VIDEO_TYPES = {
    "tutorial": "Step-by-step teaching or instructional content",
    "lecture": "Structured educational lecture or classroom-style teaching",
    "coding_tutorial": "Programming or software development demonstrated through code",
    "interview": "Conversation primarily structured as questions and answers",
    "podcast": "Long-form conversational or discussion-based content",
    "conceptual_explanation": "Explanation of concepts, theories, or ideas without being primarily a step-by-step tutorial",
    "news": "News, current events, or commentary about events",
    "other": "Does not clearly fit any of the above categories",
}

def classify_video(transcript_text: str):
    with TypeSafeClient() as client:
        result = client.system_one(
            state = {
                "transcript": transcript_text
            },
            questions = {
                "video_type": Choice(
                    instructions = """
                        Classify the primary type of this YouTube video.
                        
                        Choose the category that best describes the overall content.
                        Focus on the speaker is primarily doing in the video,
                        not isolated sections.
                    """,
                    
                    criteria = VIDEO_TYPES,
                )
            },
        )
        
    return result.choices["video_type"]