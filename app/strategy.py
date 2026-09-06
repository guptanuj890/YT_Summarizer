DIRECT_TOKEN_LIMIT = 8000

def decide_strategy(token_count: int)->str:
    if token_count <= DIRECT_TOKEN_LIMIT:
        return "direct"
    
    return "chunked"