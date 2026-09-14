import streamlit as st

from graph import build_graph


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
                "raw_transcript": [],
                "transcript_text": "",
                "token_count": 0,
                "strategy": "",
                "error": None,
                "lesson_draft": None,
                "chunks": [],
                "chunk_summaries": [],
                "final_lesson_md": ""
            }

            result = graph.invoke(
                initial_state,
                config={
                    "configurable": {
                        "thread_id": youtube_url
                    }
                }
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

                # Save lesson in session state
                st.session_state.lesson = result["lesson_draft"]
                st.session_state.video_id = result["video_id"]

                st.success(
                    "Your lesson is ready!"
                )


# --------------------------------------------------
# Display Lesson
# --------------------------------------------------

lesson = st.session_state.lesson
video_id = st.session_state.video_id


if lesson is not None:

    st.divider()

    st.header(lesson.title)


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


    # --------------------------------------------------
    # Examples
    # --------------------------------------------------

    if include_examples:

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

    if include_quiz:

        st.subheader("🧠 Quiz")

        for i, question in enumerate(
            lesson.quiz,
            1
        ):

            st.markdown(
                f"### {i}. {question.question}"
            )

            # user_answer = st.text_input(
            #     "Your answer",
            #     key=f"quiz_answer_{i}"
            # )

            # For now, always show the answer
            st.info(
                f"**Answer:** {question.answer}"
            )

            # if st.button(
            #     "Check Answer",
            #     key=f"check_{i}"
            # ):

            #     if not user_answer.strip():

            #         st.warning(
            #             "Please enter an answer first."
            #         )

            #     else:

            #         st.success(
            #             "Answer checked!"
            #         )