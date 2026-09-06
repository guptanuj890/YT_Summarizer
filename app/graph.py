from langgraph.graph import StateGraph, START, END
from state import LessonState
from nodes import extract_video_id_node, fetch_transcript_node, handle_error_node, count_tokens_node, decide_strategy_node, summarize_direct_node, chunk_transcript_node

def route_for_error(state: LessonState)->str:
    if state["error"]:
        return "error"
    
    return "success"

def route_strategy(state: LessonState)->str:
    return state["strategy"]

def build_graph():
    graph = StateGraph(LessonState)
    graph.add_node("extract_video_id", extract_video_id_node)
    graph.add_node("fetch_transcript", fetch_transcript_node)
    graph.add_node("handle_error", handle_error_node)
    graph.add_node("count_tokens", count_tokens_node)
    graph.add_node("decide_strategy", decide_strategy_node)
    graph.add_node("summarize_direct", summarize_direct_node)
    graph.add_node("chunk_transcript", chunk_transcript_node)
    
    graph.add_edge(START, "extract_video_id")
    graph.add_conditional_edges(
        "extract_video_id",
        route_for_error,
        {
            "success": "fetch_transcript",
            "error": "handle_error"
        }
    )
    graph.add_conditional_edges(
        "fetch_transcript",
        route_for_error,
        {
            "success": "count_tokens",
            "error": "handle_error"
        }
    )
    graph.add_edge("count_tokens", "decide_strategy")
    graph.add_conditional_edges(
        "decide_strategy",
        route_strategy,
        {
            "direct": "summarize_direct",
            "chunked": "chunk_transcript"
        }
    )
    graph.add_edge("summarize_direct", END)
    graph.add_edge("chunk_transcript", END)
    graph.add_edge("handle_error", END)
    
    return graph.compile()