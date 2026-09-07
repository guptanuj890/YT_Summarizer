from state import LessonState, ChunkState
from youtube import extract_video_id
from transcript import fetch_transcript, transcript_to_text
from tokenizer import count_tokens
from strategy import decide_strategy
from llm import summarize_transcript, summarize_chunk, synthesize_lesson
from chunking import chunk_transcript


def extract_video_id_node(state: LessonState)->LessonState:
    try:
        video_id = extract_video_id(state["video_url"])
        return {
            **state,
            "video_id": video_id
        }
        
    except ValueError as e:
        return {
            **state,
            "error": str(e)
        }
    
    
def fetch_transcript_node(state: LessonState)->LessonState:
    try:
        raw_transcript = fetch_transcript(state["video_id"])
        transcript_text = transcript_to_text(raw_transcript)
        
        return {
            **state,
            "raw_transcript": raw_transcript,
            "transcript_text": transcript_text
        }
    except ValueError as e:
        return {
            **state,
            "error": str(e)
        }
        
def count_tokens_node(state: LessonState)-> LessonState:
    token_count = count_tokens(state["transcript_text"])
    
    return {
        **state,
        "token_count": token_count
    }
    
def decide_strategy_node(state: LessonState)-> LessonState:
    strategy = decide_strategy(state["token_count"])
    
    return {
        **state,
        "strategy": strategy
    }

def summarize_direct_node(state: LessonState)->LessonState:
    lesson = summarize_transcript(state["transcript_text"])
    
    return {
        **state,
        "lesson_draft": lesson
    }

def chunk_transcript_node(state: LessonState)->LessonState:
    chunks = chunk_transcript(state["raw_transcript"])
    
    return {
        **state,
        "chunks": chunks
    }

def handle_error_node(state: LessonState)->LessonState:
    print(f"\nError: {state['error']}")
    
    return state

def summarize_chunk_node(state: ChunkState):
    summary = summarize_chunk(state["chunk"])
    
    return{
        "chunk_summaries": [summary]
    }
    
def reduce_synthesize_node(state:LessonState)-> LessonState:
    lesson = synthesize_lesson(state["chunk_summaries"])
    
    return {
        **state,
        "lesson_draft": lesson
    }