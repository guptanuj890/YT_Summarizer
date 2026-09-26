import streamlit as st
import uuid

from graph import build_graph
from chat import answer_doubt


st.set_page_config(
    page_title="YouTube Lesson Agent",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "lesson" not in st.session_state:
    st.session_state.lesson = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "lesson_settings" not in st.session_state:
    st.session_state.lesson_settings = None

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --------------------------------------------------
# Graph
# --------------------------------------------------

graph = build_graph()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("YouTube Lesson Agent")

st.write(
    "Turn a YouTube video into a structured lesson "
    "without watching the entire video."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Lesson Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

include_examples = st.sidebar.checkbox(
    "Include Examples",
    value=True
)

include_quiz = st.sidebar.checkbox(
    "Include Quiz",
    value=True
)


# --------------------------------------------------
# YouTube URL
# --------------------------------------------------

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

generate_button = st.button(
    "Generate Lesson",
    type="primary"
)


# --------------------------------------------------
# Generate Lesson
# --------------------------------------------------

if generate_button:

    if not youtube_url:

        st.error("Please enter a YouTube URL.")

    else:

        with st.status(
            "Generating your lesson...",
            expanded=True
        ) as status:

            st.write("Starting LangGraph...")

            initial_state = {
                "video_url": youtube_url,
                "video_id": "",
                "difficulty": difficulty,
                "include_examples": include_examples,
                "include_quiz": include_quiz,
                "raw_transcript": [],
                "transcript_text": "",
                "token_count": 0,
                "strategy": "",
                "chunks": [],
                "chunk_summaries": [],
                "lesson_draft": None,
                "final_lesson_md": "",
                "error": None,
                "video_type": ""
            }
            
            progress_placeholder = st.empty()

            progress_steps = {
                "extract_video_id": "🎬 Extracting video ID",
                "fetch_transcript": "📝 Fetching transcript",
                "classify_video_type": "Understanding video type",
                "count_tokens": "🔢 Counting tokens",
                "decide_strategy": "🧠 Selecting processing strategy",
                "chunk_transcript": "✂️ Splitting transcript",
                "summarize_direct": "🤖 Generating lesson",
                "summarize_chunk": "🤖 Processing transcript chunks",
                "reduce_synthesize": "📚 Combining lesson",
                "format_output": "✨ Formatting lesson",
                "handle_error": "❌ Handling error",
            }

            result = {}

            completed_steps = []
            

            for event in graph.stream(
                initial_state,
                config={
                    "configurable": {
                        "thread_id": str(uuid.uuid4())
                    }
                },
                stream_mode="updates"
            ):

                for node_name, update in event.items():

                    if node_name in progress_steps:
                        step_name = progress_steps[node_name]

                        if step_name not in completed_steps:
                            completed_steps.append(step_name)

                    result.update(update)

                    progress_placeholder.markdown(
                        "\n".join(
                            f"✅ {step}"
                            for step in completed_steps
                        )
                    )

            if result["error"]:

                status.update(
                    label="Generation failed",
                    state="error"
                )

                st.error(result["error"])

            else:

                status.update(
                    label="Lesson generated!",
                    state="complete"
                )

                # ------------------------------------------
                # Save generated lesson
                # ------------------------------------------

                st.session_state.lesson = result["lesson_draft"]

                st.session_state.video_id = result["video_id"]

                # IMPORTANT:
                # Save the settings that were actually used
                # for this generated lesson.
                st.session_state.lesson_settings = {
                    "difficulty": result["difficulty"],
                    "include_examples": result["include_examples"],
                    "include_quiz": result["include_quiz"],
                }

                st.success(
                    "Your lesson is ready!"
                )


# --------------------------------------------------
# Display Lesson
# --------------------------------------------------

lesson = st.session_state.lesson
video_id = st.session_state.video_id
lesson_settings = st.session_state.lesson_settings


if lesson is not None and lesson_settings is not None:

    st.divider()

    st.header(lesson.title)
    # --------------------------------------------------
    # Key Takeaways
    # --------------------------------------------------

    if lesson.key_takeaways:

        st.subheader("🎯 Key Takeaways")

        for takeaway in lesson.key_takeaways:
            st.markdown(
                f"- {takeaway}"
            )
    
    # --------------------------------------------------
    # Show Generated Settings
    # --------------------------------------------------

    st.caption(
        f"Difficulty: {lesson_settings['difficulty']}"
    )


    # --------------------------------------------------
    # Key Concepts
    # --------------------------------------------------

    st.subheader("📚 Key Concepts")

    for concept in lesson.concepts:

        st.markdown(
            f"### {concept.name}"
        )

        st.write(
            concept.explanation
        )

        for source in concept.sources:

            timestamp = int(source.timestamp)

            minutes = timestamp // 60
            seconds = timestamp % 60

            youtube_link = (
                f"https://www.youtube.com/watch?"
                f"v={video_id}&t={timestamp}s"
            )

            st.markdown(
                f"📍 [{minutes}:{seconds:02d}]"
                f"({youtube_link}) — "
                f"{source.description}"
            )

    if any(concept.analogy for concept in lesson.concepts):
        st.subheader("Analogies")
        for concept in lesson.concepts:
            if concept.analogy:
                st.markdown(f"**{concept.name}**")
                st.markdown(f"- {concept.analogy}")

        
    # --------------------------------------------------
    # Examples
    # --------------------------------------------------

    if lesson_settings["include_examples"]:

        st.subheader("💡 Examples")

        for example in lesson.examples:

            st.write(
                f"• {example.description}"
            )

            for source in example.sources:

                timestamp = int(source.timestamp)

                minutes = timestamp // 60
                seconds = timestamp % 60

                youtube_link = (
                    f"https://www.youtube.com/watch?"
                    f"v={video_id}&t={timestamp}s"
                )

                st.markdown(
                    f"  - 📍 [{minutes}:{seconds:02d}]"
                    f"({youtube_link}) — "
                    f"{source.description}"
                )


    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    st.subheader("📝 Summary")

    st.write(
        lesson.summary
    )

    # --------------------------------------------------
    # Quiz
    # --------------------------------------------------

    if lesson_settings["include_quiz"]:

        st.subheader("🧠 Quiz")

        for i, question in enumerate(
            lesson.quiz,
            1
        ):

            st.markdown(
                f"### {i}. {question.question}"
            )

            # For now, always show the answer
            st.info(
                f"**Answer:** {question.answer}"
            )
            
            
    if lesson.follow_up_questions:
        st.subheader("Folow Up Questions....")
        
        for i, question in enumerate (lesson.follow_up_questions, 1):
            st.markdown(f"**{i}.** {question}")
            
            
    st.divider()
    
    st.subheader("Ask Doubts....")
    
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask anything about this lesson..."
    )

    if question:

        st.session_state.chat_messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = answer_doubt(
                    question,
                    lesson,
                    lesson_settings["difficulty"],
                    st.session_state.chat_messages
                )

            st.markdown(answer)

        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": answer
        })