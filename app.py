
import streamlit as st
from streamlit_ace import st_ace
from PyPDF2 import PdfReader

from resume_parsar import extract_resume_sections
from question_generater import generate_questions
from voice import audio_recording, transcribe_audio
from evaluation_agent import evaluate_answer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Mock Interviewer",
    layout="centered"
)


# ---------------- SESSION STATE ----------------
defaults = {
    "stage": "setup",
    "questions": [],
    "current_question": 0,
    "answers": {},
    "skills": [],
    "projects": [],
    "experience": [],
    "audio_key": 0,
    "temp_transcript": "",
    "evaluations": {},
    "scores": {},
}

for key, default_value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


# ---------------- HEADER ----------------
st.title("AI Mock Interviewer")
st.write("Welcome to the AI Mock Interviewer!")


# ---------------- SIDEBAR ----------------
st.sidebar.header("Student Credentials")

name = st.sidebar.text_input("Please enter your name:")

role = st.sidebar.selectbox(
    "Please select the role you are interviewing for:",
    [
        "Software Engineer",
        "Data Analyst",
        "Machine Learning Engineer",
        "Data Scientist",
        "Product Manager",
    ],
)

uploaded_file = st.sidebar.file_uploader(
    "Upload your resume (PDF):",
    type=["pdf"],
)

process_resume = st.sidebar.button("Process Resume")

resume_text = ""

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text

        st.sidebar.success("Resume uploaded successfully!")

    except Exception as error:
        st.sidebar.error(f"Could not read PDF: {error}")


# ---------------- PROCESS RESUME ----------------
if process_resume:
    if not name.strip():
        st.sidebar.warning("Please enter your name.")

    elif uploaded_file is None:
        st.sidebar.warning("Please upload your resume.")

    elif not resume_text.strip():
        st.sidebar.warning(
            "No readable text found in this PDF. "
            "Please upload a text-based PDF."
        )

    else:
        try:
            with st.spinner("Processing resume and generating questions..."):
                skills, projects, experience = extract_resume_sections(
                    resume_text
                )

                questions = generate_questions(
                    role,
                    skills,
                    projects,
                    experience
                )

            if not questions:
                st.sidebar.error(
                    "No questions generated. Please try again."
                )

            else:
                st.session_state.questions = questions
                st.session_state.skills = skills
                st.session_state.projects = projects
                st.session_state.experience = experience

                # Reset previous interview data
                st.session_state.answers = {}
                st.session_state.current_question = 0
                st.session_state.temp_transcript = ""
                st.session_state.evaluations = {}
                st.session_state.scores = {}
                st.session_state.audio_key += 1

                st.session_state.stage = "summary"
                st.rerun()

        except Exception as error:
            st.sidebar.error(
                f"Resume processing failed: {error}"
            )


# ---------------- CANDIDATE SUMMARY ----------------
if st.session_state.stage == "summary":
    st.divider()
    st.subheader("Candidate Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Skills")

        if st.session_state.skills:
            for skill in st.session_state.skills:
                st.write("•", skill)
        else:
            st.write("No skills detected")

    with col2:
        st.subheader("Projects")

        if st.session_state.projects:
            for project in st.session_state.projects:
                st.write("•", project)
        else:
            st.write("No projects detected")

    with col3:
        st.subheader("Experience")

        if st.session_state.experience:
            for item in st.session_state.experience:
                st.write("•", item)
        else:
            st.write("No experience detected")

    st.divider()

    if st.button("Begin Interview", type="primary"):
        st.session_state.current_question = 0
        st.session_state.temp_transcript = ""
        st.session_state.audio_key += 1
        st.session_state.stage = "interview"
        st.rerun()


# ---------------- INTERVIEW ----------------
if st.session_state.stage == "interview":

    questions = st.session_state.questions
    current_question = st.session_state.current_question
    total_questions = len(questions)

    if total_questions == 0:
        st.error(
            "No questions available. Please process your resume again."
        )
        st.stop()

    if not 0 <= current_question < total_questions:
        st.session_state.current_question = 0
        st.rerun()

    question = questions[current_question]

    st.progress((current_question + 1) / total_questions)

    st.subheader(
        f"Question {current_question + 1} of {total_questions}"
    )

    st.write(question)
    st.divider()

    # First two questions: coding editor
    if current_question < 2:

        st.write("Write your code below:")

        language = st.selectbox(
            "Select programming language:",
            ["Python", "JavaScript", "Java", "C++", "Go"],
            key=f"lang_{current_question}",
        )

        language_map = {
            "Python": "python",
            "JavaScript": "javascript",
            "Java": "java",
            "C++": "cpp",
            "Go": "golang",
        }

        answer = st_ace(
            value=st.session_state.answers.get(
                current_question, ""
            ),
            language=language_map[language],
            theme="monokai",
            height=320,
            auto_update=True,
            key=f"code_editor_{current_question}",
        )

        if answer is None:
            answer = ""

        st.session_state.answers[current_question] = answer

    # Remaining questions: audio recording
    else:

        st.write("Record your answer below:")

        audio = audio_recording(
            key=f"audio_{current_question}_{st.session_state.audio_key}"
        )

        if audio is not None and len(audio) > 0:

            st.success("Recording received!")

            # Listen to your recording before transcription
            st.write("Listen to your recording:")
            st.audio(
                audio.export().read(),
                format="audio/wav"
            )

            if st.button(
                "Transcribe Recording",
                key=f"transcribe_{current_question}_{st.session_state.audio_key}",
            ):
                with st.spinner("Transcribing your answer..."):
                    text = transcribe_audio(audio)

                if text and text.strip():
                    st.session_state.temp_transcript = text.strip()
                    st.success("Transcription completed!")

                else:
                    st.warning(
                        "No speech detected. Please check the recording "
                        "and try again."
                    )

        # Show the latest transcript
        if st.session_state.temp_transcript:
            st.subheader("Transcribed Text")
            st.write(st.session_state.temp_transcript)

            if st.button(
                "Save Recording as Answer",
                key=f"save_{current_question}_{st.session_state.audio_key}",
            ):
                st.session_state.answers[current_question] = (
                    st.session_state.temp_transcript
                )
                st.success("Answer saved successfully!")

        # Show previously saved answer
        if current_question in st.session_state.answers:
            st.divider()
            st.subheader("Saved Answer")
            st.write(
                st.session_state.answers[current_question]
            )

    # ---------------- NAVIGATION ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Previous Question",
            disabled=(current_question == 0),
        ):
            st.session_state.current_question -= 1
            st.session_state.audio_key += 1
            st.session_state.temp_transcript = ""
            st.rerun()

    with col2:
        if st.button("Next Question", type="primary"):

            if current_question < total_questions - 1:
                st.session_state.current_question += 1
                st.session_state.audio_key += 1
                st.session_state.temp_transcript = ""
                st.rerun()

            else:
                st.session_state.stage = "results"
                st.rerun()


# ---------------- RESULTS ----------------
if st.session_state.stage == "results":

    st.subheader("Interview Completed")

    total_questions = len(st.session_state.questions)
    total_score = 0

    for i, question in enumerate(st.session_state.questions):

        st.subheader(f"Question {i + 1}")
        st.write(question)

        answer = st.session_state.answers.get(i, "")

        st.write("Answer:")
        st.write(answer if answer else "No answer provided")

        if not answer:

            evaluation = (
                "Result: Not Answered\n"
                "Score: 0/10\n"
                "Feedback: No response was provided.\n"
                "Improvement: Attempt the question to receive evaluation."
            )

            st.session_state.evaluations[i] = evaluation
            st.session_state.scores[i] = 0

        elif i not in st.session_state.evaluations:

            try:
                with st.spinner(
                    f"Evaluating question {i + 1}..."
                ):
                    evaluation = evaluate_answer(
                        question,
                        answer,
                        i
                    )

                st.session_state.evaluations[i] = evaluation

                score = 0

                if "Score:" in evaluation:
                    try:
                        score_text = evaluation.split(
                            "Score:", 1
                        )[1]

                        score_value = score_text.split(
                            "/", 1
                        )[0]

                        score = int(float(score_value.strip()))

                    except (ValueError, IndexError):
                        score = 0

                st.session_state.scores[i] = max(
                    0, min(score, 10)
                )

            except Exception as error:
                st.session_state.evaluations[i] = (
                    f"Evaluation failed: {error}"
                )
                st.session_state.scores[i] = 0

        st.info("Evaluation:")
        st.write(st.session_state.evaluations[i])

        total_score += st.session_state.scores.get(i, 0)

        st.divider()

    if total_questions > 0:
        percentage = (
            total_score / (total_questions * 10)
        ) * 100

        st.success(f"Final Score: {percentage:.1f}%")

    else:
        st.warning("No questions were evaluated.")

    if st.button("Start a New Interview"):

        st.session_state.stage = "setup"
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.session_state.skills = []
        st.session_state.projects = []
        st.session_state.experience = []
        st.session_state.temp_transcript = ""
        st.session_state.evaluations = {}
        st.session_state.scores = {}
        st.session_state.audio_key += 1

        st.rerun()
