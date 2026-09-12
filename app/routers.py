from state import LessonState
from langgraph.types import Send

def route_for_error(state: LessonState)->str:
    if state["error"]:
        return "error"
    
    return "success"

def route_strategy(state: LessonState)->str:
    return state["strategy"]

def fan_out_chunks(state:LessonState):
    return [
        Send(
            "summarize_chunk",
            {"chunk": chunk}
        )
        for chunk in state["chunks"]
    ]
