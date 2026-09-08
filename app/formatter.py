from schema import LessonDraft

def format_lesson_markdown(lesson: LessonDraft)-> str:
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
        
    if lesson.examples:
        lines.append("## Examples")
        lines.append("")
        
        for example in lesson.examples:
            lines.append(f"- {example.description}")
            
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