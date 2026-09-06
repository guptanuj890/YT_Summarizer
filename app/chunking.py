import tiktoken

CHUNK_TOKEN_LIMIT = 4000

def chunk_transcript(segments: list[dict])-> list[str]:
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for segment in segments:
        text = segment["text"]
        start = segment["start"]
        
        segment_text = f"[{start:.1f}s] {text}"
        segment_tokens = len(encoding.encode(segment_text))
        
        if(current_chunk and current_tokens + segment_tokens > CHUNK_TOKEN_LIMIT):
            chunks.append("\n".join(current_chunk))
            current_chunk = []
            current_tokens = 0
            
        current_chunk.append(segment_text)
        current_tokens += segment_tokens
        
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks