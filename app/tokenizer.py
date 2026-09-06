import tiktoken

def count_tokens(text: str, model: str = "gpt-4o")-> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    
    return len(tokens)