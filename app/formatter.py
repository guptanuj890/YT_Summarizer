from schema import LessonDraft

def format_timestamp(timestamp: float, video_id:str)-> str:
    total_seconds = int(timestamp)
    
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    url = (
        f"https://www.youtube.com/watch?v={video_id}"
        f"&t={total_seconds}s"
    )
    
    return f"[{minutes}:{seconds:02d}]({url})"

def format_lesson_markdown(lesson: LessonDraft, video_id: str)-> str:
    lines = []
    
    lines.append(f"#{lesson.title}")
    lines.append("")
    
    lines.append("# Key Concepts")
    lines.append("")
    
    for concept in lesson.concepts:
        lines.append(f"###{concept.name}")
        lines.append("")
        lines.append(concept.explanation)
        lines.append("")
        
        if concept.sources:
            lines.append("**Sources**")
            for source in concept.sources:
                timestamp = format_timestamp(
                    source.timestamp,
                    video_id
                )
                
                lines.append(
                    f"- '{timestamp} - {source.description}"
                )
                
            lines.append("")
                
        
    if lesson.examples:
        lines.append("## Examples")
        lines.append("")
        
        for example in lesson.examples:
            lines.append(f"- {example.description}")
            
            if example.sources:
                for source in example.sources:
                    timestamp = format_timestamp(
                        source.timestamp,
                        video_id
                    )
                    
                    lines.append(
                        f" - '{timestamp} - {source.description}"
                    )
                
            lines.append("")
        
    lines.append("## Summary")
    lines.append("")
    lines.append(lesson.summary)
    lines.append("")
    
    if lesson.quiz:
        lines.append("## Quiz")
        lines.append("")
        
        for i, question in enumerate(lesson.quiz, 1):
            lines.append(f"### {i}. {question.question}")
            lines.append("")
            lines.append(f"**Answer:** {question.answer}")
            lines.append
            
    return "\n".join(lines)