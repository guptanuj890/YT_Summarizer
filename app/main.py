from youtube import extract_video_id
from transcript import fetch_transcript, transcript_to_text
from llm import generate_lesson

def main():
    url = input("Enter the YouTube URL:")
    
    try:
        video_id = extract_video_id(url)
        print("video_id:", video_id)
        
        raw_transcript = fetch_transcript(video_id)
        transcript_text = transcript_to_text(raw_transcript)
        
        print(f"Transcript segments: {len(raw_transcript)}")
        print(f"Transcript Characters: {len(transcript_text)}")
        
        print("\nGenerating lesson...\n")
        
        lesson = generate_lesson(transcript_text)
        print(lesson)
        
    except ValueError as e:
        print("Error:", e)
        
    except Exception as e:
        print("Transcript error:", e)

if __name__ == "__main__":
    main()