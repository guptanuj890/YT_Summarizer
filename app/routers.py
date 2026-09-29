from state import LessonState
from langgraph.types import Send

def route_for_error(state: LessonState)->str:
    if state["error"]:
        return "error"
    
    return "success"

def route_strategy(state: LessonState)->str:
    return state["strategy"]

def fan_out_chunks(state: LessonState):
    from langgraph.types import Send

    return [
        Send(
            "summarize_chunk",
            {
                "chunk": chunk,
                "difficulty": state["difficulty"],
                "include_examples": state["include_examples"],
                "include_quiz": state["include_quiz"],
                "chunk_errors": [],
            }
        )
        for chunk in state["chunks"]
    ]


def route_after_chunks(state: LessonState) -> str:
    if state.get("chunk_errors"):
        state["error"] = (
            f"{len(state['chunk_errors'])} transcript chunk(s) failed. "
            + " | ".join(state["chunk_errors"])
        )
        return "error"

    return "success"