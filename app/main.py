from graph import build_graph

def main():
    url = input("Enter YouTube video Link: ")
    
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
    result = graph.invoke(initial_state)
    
    # print("video_id:", result["video_id"])
    
    # print("transcript_text:", result["transcript_text"])
    # print("Tokens:", result["token_count"])
    # print("strategy: ", result["strategy"])
    if result["final_lesson_md"]:
        print("\n==========LESSON=========\n")
        print(result["final_lesson_md"])
    # for i, chunk in enumerate(result["chunk_summaries"]):
    #     print(f"\n=======CHUNK Summaries {i+1} =======\n")
    #     print(chunk[:500])
    
    
if __name__ == "__main__":
    main()