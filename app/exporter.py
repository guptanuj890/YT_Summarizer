import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch

def lesson_to_pdf(
    lesson,
    video_id: str,
    chat_messages=None,
    output_path="lesson.pdf"
):
    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    subheading_style = styles["Heading3"]
    body_style = styles["BodyText"]

    story = []

    # Title
    story.append(Paragraph(lesson.title, title_style))
    story.append(Spacer(1, 20))

    # Key Takeaways
    if lesson.key_takeaways:
        story.append(Paragraph("🎯 Key Takeaways", heading_style))
        story.append(Spacer(1, 8))

        for takeaway in lesson.key_takeaways:
            story.append(
                Paragraph(f"• {takeaway}", body_style)
            )
            story.append(Spacer(1, 5))

    # Concepts
    story.append(Paragraph("📚 Key Concepts", heading_style))
    story.append(Spacer(1, 8))

    for concept in lesson.concepts:
        story.append(
            Paragraph(concept.name, subheading_style)
        )
        story.append(Spacer(1, 5))

        story.append(
            Paragraph(concept.explanation, body_style)
        )
        story.append(Spacer(1, 8))

        if concept.analogy:
            story.append(
                Paragraph(
                    f"<b>💡 Analogy:</b> {concept.analogy}",
                    body_style
                )
            )
            story.append(Spacer(1, 8))

    # Examples
    if lesson.examples:
        story.append(
            Paragraph("💡 Examples", heading_style)
        )
        story.append(Spacer(1, 8))

        for example in lesson.examples:
            story.append(
                Paragraph(
                    f"• {example.description}",
                    body_style
                )
            )
            story.append(Spacer(1, 5))

    # Summary
    story.append(
        Paragraph("📝 Summary", heading_style)
    )
    story.append(Spacer(1, 8))

    story.append(
        Paragraph(lesson.summary, body_style)
    )
    story.append(Spacer(1, 15))

    # Doubts & Answers
    if chat_messages:
        story.append(
            Paragraph(
                "💬 Doubts & Answers",
                heading_style
            )
        )
        story.append(Spacer(1, 8))

        for message in chat_messages:

            if message["role"] == "user":
                story.append(
                    Paragraph(
                        "<b>❓ Doubt</b>",
                        subheading_style
                    )
                )
                story.append(Spacer(1, 5))

                story.append(
                    Paragraph(
                        message["content"],
                        body_style
                    )
                )
                story.append(Spacer(1, 10))

            elif message["role"] == "assistant":
                story.append(
                    Paragraph(
                        "<b>🤖 Answer</b>",
                        subheading_style
                    )
                )
                story.append(Spacer(1, 5))

                story.append(
                    Paragraph(
                        message["content"],
                        body_style
                    )
                )
                story.append(Spacer(1, 15))

    # Build PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    doc.build(story)


def safe_filename(title: str) -> str:

    title = re.sub(
        r'[<>:"/\\|?*]',
        "",
        title
    )

    title = title.strip()

    return title[:100]

def lesson_to_markdown(lesson, video_id: str, chat_messages=None) -> str:

    lines = []

    lines.append(f"# {lesson.title}")
    lines.append("")

    # Key Takeaways
    if lesson.key_takeaways:
        lines.append("## 🎯 Key Takeaways")
        lines.append("")

        for takeaway in lesson.key_takeaways:
            lines.append(f"- {takeaway}")

        lines.append("")

    # Concepts
    lines.append("## 📚 Key Concepts")
    lines.append("")

    for concept in lesson.concepts:

        lines.append(f"### {concept.name}")
        lines.append("")
        lines.append(concept.explanation)
        lines.append("")

        if concept.analogy:
            lines.append(
                f"**💡 Analogy:** {concept.analogy}"
            )
            lines.append("")

        for source in concept.sources:

            timestamp = int(source.timestamp)
            minutes = timestamp // 60
            seconds = timestamp % 60

            youtube_link = (
                f"https://www.youtube.com/watch?"
                f"v={video_id}&t={timestamp}s"
            )

            lines.append(
                f"📍 [{minutes}:{seconds:02d}]"
                f"({youtube_link}) — "
                f"{source.description}"
            )

            lines.append("")

    # Examples
    if lesson.examples:

        lines.append("## 💡 Examples")
        lines.append("")

        for example in lesson.examples:

            lines.append(
                f"- {example.description}"
            )

            for source in example.sources:

                timestamp = int(source.timestamp)
                minutes = timestamp // 60
                seconds = timestamp % 60

                youtube_link = (
                    f"https://www.youtube.com/watch?"
                    f"v={video_id}&t={timestamp}s"
                )

                lines.append(
                    f"  - 📍 [{minutes}:{seconds:02d}]"
                    f"({youtube_link}) — "
                    f"{source.description}"
                )

            lines.append("")

    # Summary
    lines.append("## 📝 Summary")
    lines.append("")
    lines.append(lesson.summary)
    lines.append("")

    if chat_messages:
        lines.append("## 💬 Doubts & Answers")
        lines.append("")

        for message in chat_messages:
            if message["role"] == "user":
                lines.append(f"### ❓ Doubt")
                lines.append("")
                lines.append(message["content"])
                lines.append("")

            elif message["role"] == "assistant":
                lines.append("### 🤖 Answer")
                lines.append("")
                lines.append(message["content"])
                lines.append("")
    
    # # Quiz
    # if lesson.quiz:

    #     lines.append("## 🧠 Quiz")
    #     lines.append("")

    #     for i, question in enumerate(
    #         lesson.quiz, 1
    #     ):
    #         lines.append(
    #             f"### {i}. {question.question}"
    #         )
    #         lines.append("")
    #         lines.append(
    #             f"**Answer:** {question.answer}"
    #         )
    #         lines.append("")

    # # Follow-up Questions
    # if lesson.follow_up_questions:

    #     lines.append("## 🔍 Explore Further")
    #     lines.append("")

    #     for i, question in enumerate(
    #         lesson.follow_up_questions, 1
    #     ):
    #         lines.append(
    #             f"{i}. {question}"
    #         )

    #     lines.append("")

    return "\n".join(lines)