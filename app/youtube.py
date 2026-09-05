from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str)->str:
    parsed = urlparse(url)
    
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed.path =="/watch":
            video_id = parse_qs(parsed.query).get("v")
            
            if video_id:
                return video_id[0]
            
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]
        
    if parsed.hostname == "youtu.be":
        return parsed.path.strip("/").split("/")[0]
    
    raise ValueError("Invalid or unsupported Youtbe URL")