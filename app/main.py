from graph import build_graph
import uuid

def main():
    
    url = input("Enter YouTube video Link: ")
    
    thread_id = str(uuid.uuid4())
    
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    graph = build_graph()
    
    initial_state = {
        "video_url": url,
        "video_id": "",
        "raw_transcript": [],
        "transcript_text": "",
        "token_count": 0,
        "strategy": "",
        "error": None,
        "lesson_draft": None,
        "chunks": [],
        "chunk_summaries": [],
        "final_lesson_md": ""
    }
    # print(initial_state["video_url"])
    result = graph.invoke(
        initial_state,
        config = config
    )
    
    
    if result["final_lesson_md"]:
        print("\n==========LESSON=========\n")
        print(result["final_lesson_md"])
    
    
if __name__ == "__main__":
    main()