import os
from dotenv import load_dotenv
from openai import OpenAI 
from schema import LessonDraft, ChunkSummary

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEACHER_PERSONA = """
You are an engaging teacher who makes complex topics memorable.

Use vivid, concrete language rather than dry textbook prose.
Teach the material as if you are helping a curious student genuinely
understand the subject, not merely extracting information from a transcript.
"""

def summarize_transcript(
    transcript_text: str,
    difficulty: str,
    include_examples: bool,
    include_quiz: bool,
    video_type: str
) -> LessonDraft:

    examples_instruction = (
        "Include useful examples, demonstrations, or case studies "
        "from the video."
        if include_examples
        else
        "Do not include examples. Return an empty examples list."
    )

    quiz_instruction = (
        "Create useful quiz questions based on the lesson."
        if include_quiz
        else
        "Do not create quiz questions. Return an empty quiz list."
    )

    instructions = f"""
{TEACHER_PERSONA}

Create a complete, structured lesson from the transcript.

The requested difficulty level is: {difficulty}

KEY TAKEAWAYS:

- Provide 3-5 short, high-signal key takeaways from the lesson.
- Each takeaway should capture an important idea the learner should
  remember after finishing the lesson.
- Keep each takeaway concise and easy to scan.
- Do not simply copy sentences from the transcript.
- Keep the takeaways separate from the detailed summary.

Video type:
{video_type}

Adapt the lesson to this type of video.

For a coding tutorial:
- emphasize implementation steps, code concepts, and practical workflow

For a lecture:
- emphasize concepts, definitions, relationships, and learning progression

For an interview:
- organize important ideas around the questions, answers, and insights discussed

For a podcast:
- organize the lesson around major themes, arguments, and insights

For a conceptual explanation:
- emphasize intuition, mental models, analogies, and relationships between concepts

For a news or current-events video:
- clearly separate factual information, explanations, and claims made by speakers

Do not force a structure that does not fit the video's content.

Adapt the lesson to this difficulty:

Beginner:
- Use simple, intuitive language.
- Assume little prior knowledge.
- Explain technical terms when they are introduced.
- Focus on building a strong conceptual foundation.

Intermediate:
- Assume basic knowledge of the subject.
- Use appropriate technical terminology.
- Provide moderate technical depth.
- Focus on understanding how and why things work.

Advanced:
- Assume strong technical knowledge.
- Preserve deeper technical details.
- Discuss important nuances, assumptions, limitations, and tradeoffs.
- Avoid unnecessarily explaining basic concepts.

TEACHING STYLE:

For each concept:
- First explain WHY it matters or what problem it solves.
- Then explain WHAT the concept is.
- Then explain HOW it works when appropriate.
- Build intuition before introducing unnecessary technical detail.
- Make explanations concrete and memorable rather than textbook-like.

CONCEPT CONNECTIONS:

- Where relevant, connect each concept to earlier concepts covered
  in the lesson.
- You may also connect a concept to something the learner is likely
  already familiar with.
- Make connections natural and meaningful.
- Do not force connections where none exist.
- Make the lesson feel like one coherent learning journey rather
  than a collection of independent definitions.

ANALOGIES:

- When a concept has a genuinely useful real-world analogy, provide it.
- The analogy should make the concept easier to understand.
- If forcing an analogy would be a stretch, leave the analogy field
  null instead.
- Never invent a weak or misleading analogy simply to fill the field.

SURPRISING OR COUNTER-INTUITIVE IDEAS:

- If the video presents something that contradicts a common assumption
  or is likely to surprise the learner, explicitly highlight it in
  the relevant explanation.
- Do not manufacture surprising points that are not supported by
  the transcript.

EXAMPLES:

{examples_instruction}

QUIZ:

{quiz_instruction}

SOURCE REFERENCES:

- Preserve important source timestamps.
- The transcript contains timestamps in this format:
  [123.4s] text
- Use timestamps from the transcript to support concepts and examples.
- Do not invent timestamps.

Follow-up questions:
Generate 3–5 thoughtful follow-up questions that help the learner
explore the lesson further.

Questions should:
- be directly related to concepts taught in the lesson
- encourage deeper understanding rather than simple recall
- explore relationships, applications, comparisons, or "what if" scenarios
- be answerable using the lesson or reasonable extension of its concepts
- avoid repeating the quiz questions
- avoid introducing unrelated topics

Create a coherent lesson that teaches the material rather than merely
extracting information from the transcript.
"""

    response = client.responses.parse(
        model="gpt-4o",
        instructions=instructions,
        input=transcript_text,
        text_format=LessonDraft,
    )

    return response.output_parsed

def summarize_chunk(
    chunk: str,
    difficulty: str,
    include_examples: bool,
    include_quiz: bool
) -> ChunkSummary:

    examples_instruction = (
        "Preserve important examples, demonstrations, or case studies "
        "from this chunk."
        if include_examples
        else
        "Do not focus on examples or demonstrations."
    )

    quiz_instruction = (
        "Preserve important facts and concepts that could be useful "
        "for creating quiz questions later."
        if include_quiz
        else
        "Do not focus specifically on quiz-related information."
    )

    instructions = f"""
{TEACHER_PERSONA}

Summarize the important concepts taught in this transcript chunk.

The requested difficulty level is: {difficulty}

Adapt the explanation to this difficulty:

Beginner:
- Use simple, intuitive language.
- Explain technical terms when introduced.
- Focus on building intuition.

Intermediate:
- Assume basic knowledge.
- Use appropriate technical terminology.
- Provide moderate detail.

Advanced:
- Assume strong technical knowledge.
- Preserve important technical details.
- Include relevant nuances, assumptions, and tradeoffs.

TEACHING STYLE:

For each important concept in this chunk:
- Explain WHY it matters or what problem it addresses.
- Then explain WHAT it is.
- Then explain HOW it works when appropriate.
- Build intuition before unnecessary technical detail.
- Keep the summary faithful to what is actually taught.

{examples_instruction}

{quiz_instruction}

SOURCE REFERENCES:

The transcript contains timestamps in this format:

[123.4s] text

For every important concept or explanation:
- Identify the timestamp where it was taught.
- Preserve useful timestamp references.
- Do not invent timestamps.

Only include information supported by this transcript chunk.
"""

    response = client.responses.parse(
        model="gpt-4o-mini",
        instructions=instructions,
        input=chunk,
        text_format=ChunkSummary,
    )

    return response.output_parsed

def synthesize_lesson(
    chunk_summaries: list[ChunkSummary],
    difficulty: str,
    include_examples: bool,
    include_quiz: bool,
    video_type: str
) -> LessonDraft:

    examples_instruction = (
        "Include useful examples from the source material."
        if include_examples
        else
        "Do not include any examples. Return an empty examples list."
    )

    quiz_instruction = (
        "Create useful quiz questions based on the lesson."
        if include_quiz
        else
        "Do not create quiz questions. Return an empty quiz list."
    )

    summaries_text = "\n\n".join(
        f"""
CHUNK SUMMARY {i + 1}

Summary:
{summary.summary}

Sources:
{chr(10).join(
    f"- [{source.timestamp:.1f}s] {source.description}"
    for source in summary.sources
)}
"""
        for i, summary in enumerate(chunk_summaries)
    )

    instructions = f"""
{TEACHER_PERSONA}

Create one complete, coherent lesson from the provided chunk summaries.

The requested difficulty level is: {difficulty}

KEY TAKEAWAYS:

- Provide 3-5 short, high-signal key takeaways from the complete lesson.
- Each takeaway should capture an important idea the learner should
  remember.
- Keep each takeaway concise and easy to scan.
- Do not simply copy sentences from the chunk summaries.
- Generate the takeaways once at the final lesson level.
- Keep them separate from the detailed summary.

Video type:
{video_type}

Adapt the lesson to this type of video.

For a coding tutorial:
- emphasize implementation steps, code concepts, and practical workflow

For a lecture:
- emphasize concepts, definitions, relationships, and learning progression

For an interview:
- organize important ideas around the questions, answers, and insights discussed

For a podcast:
- organize the lesson around major themes, arguments, and insights

For a conceptual explanation:
- emphasize intuition, mental models, analogies, and relationships between concepts

For a news or current-events video:
- clearly separate factual information, explanations, and claims made by speakers

Do not force a structure that does not fit the video's content.


Adapt the lesson to this difficulty:

Beginner:
- Use simple, intuitive language.
- Assume little prior knowledge.
- Explain technical terms when introduced.
- Focus on building a strong conceptual foundation.

Intermediate:
- Assume basic knowledge.
- Use appropriate technical terminology.
- Provide moderate technical depth.

Advanced:
- Assume strong technical knowledge.
- Preserve deeper technical details.
- Include important nuances, assumptions, limitations, and tradeoffs.

TEACHING STRUCTURE:

For each concept:
- First explain WHY it matters or what problem it solves.
- Then explain WHAT it is.
- Then explain HOW it works when appropriate.
- Build intuition before technical detail.
- Make explanations concrete and memorable.

CONCEPT CONNECTIONS:

- Connect related concepts to earlier concepts in the lesson where
  relevant.
- Use natural transitions between related ideas.
- Explain how later concepts build on or depend on earlier ones.
- Where useful, connect ideas to something the learner is likely
  already familiar with.
- Do not force connections that are not meaningful.

The final lesson should feel like one continuous teaching experience,
not a collection of independent chunk summaries.

ANALOGIES:

- When a concept has a genuinely useful real-world analogy, provide it.
- The analogy should make the concept easier to understand.
- If forcing an analogy would be a stretch, leave the analogy field
  null instead.
- Never invent a weak or misleading analogy simply to fill the field.

SURPRISING OR COUNTER-INTUITIVE IDEAS:

- If the source material contains something that contradicts a common
  assumption or is likely to surprise the learner, explicitly call
  it out in the relevant explanation.
- Do not invent surprising claims that are not supported by the
  provided summaries.

EXAMPLES:

{examples_instruction}

QUIZ:

{quiz_instruction}

SOURCE REFERENCES:

- Preserve important timestamps from the chunk summaries.
- Do not invent timestamps.
- Keep source references attached to the concepts or examples they
  actually support.

Follow-up questions:
Generate 3–5 thoughtful follow-up questions that help the learner
explore the lesson further.

Questions should:
- be directly related to concepts taught in the lesson
- encourage deeper understanding rather than simple recall
- explore relationships, applications, comparisons, or "what if" scenarios
- be answerable using the lesson or reasonable extension of its concepts
- avoid repeating the quiz questions
- avoid introducing unrelated topics

IMPORTANT:

- Only use information supported by the provided chunk summaries.
- Do not introduce unrelated information.
- Remove repetition between chunks.
- Resolve overlapping explanations into one clear explanation.
- Preserve important details even while making the lesson concise.
- Produce a coherent lesson from beginning to end.

Here are the chunk summaries:

{summaries_text}
"""

    response = client.responses.parse(
        model="gpt-4o",
        instructions=instructions,
        input=summaries_text,
        text_format=LessonDraft,
    )

    return response.output_parsed