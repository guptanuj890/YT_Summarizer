from youtube_transcript_api import YouTubeTranscriptApi 
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
)

def fetch_transcript(video_id: str, languages = None):
    if languages is None:
        languages = ["en"]
        
    api = YouTubeTranscriptApi()
    
    try:
        transcipt = api.fetch(video_id, languages=languages)
        segments = []
        
        for segment in transcipt:
            segments.append({
                "text": segment.text,
                "start": segment.start,
                "duration": segment.duration
            })
            
        return segments
    
    except TranscriptsDisabled:
        raise ValueError(
            "Transcript are for this video"
        )
        
    except NoTranscriptFound:
        raise ValueError(
            f"No transcript found for languages: {languages}"
        )
        
def transcript_to_text(segments):
    return " ".join(
        segment["text"]
        for segment in segments
    )