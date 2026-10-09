# 🎯 AI Mock Interviewer

An interactive **AI-powered mock interview system** that simulates technical interviews using resume-based question generation, voice input, and automated answer evaluation.

This project helps students and job seekers practice interviews in a realistic environment by generating personalized questions, recording responses, and providing structured feedback.

---

# 🚀 Features

### 1. Resume-Based Interview Generation

* Upload a PDF resume
* Automatically extracts:

  * Skills
  * Projects
  * Experience
* Generates personalized interview questions based on the resume content

### 2. Dynamic Question Flow

* Coding and non-coding questions
* Question count adapts based on experience
* Sequential interview navigation using session state

### 3. Voice Answer Recording

* Record answers directly in the browser
* Audio is transcribed using AI speech recognition
* Supports hands-free interview practice

### 4. AI Answer Evaluation

* Evaluates responses automatically
* Provides structured feedback:

  * Result (Correct / Incorrect)
  * Score (when applicable)
  * Feedback
  * Improvement suggestion

### 5. Secure API Handling

* Uses `.env` environment variables
* API keys are protected via `.gitignore`
* Production-ready security practice

### 6. Session State Management

Maintains interview progress including:

* Current question
* User answers
* Transcriptions
* Evaluations
* Interview stage

---

# 🧠 System Architecture

User → Upload Resume → Extract Sections → Generate Questions → Record Answer → Transcribe Audio → Evaluate Answer → Show Results

---

# 🛠️ Tech Stack

Frontend

* Streamlit

Backend

* Python

AI / NLP

* Groq API (LLM)
* Whisper Speech Recognition

Libraries

* streamlit
* PyPDF2
* python-dotenv
* audiorecorder
* groq

Version Control

* Git
* GitHub

---

# 📂 Project Structure

AI-Mock-Interviewer/

app.py
Main Streamlit application

question_generater.py
Generates interview questions

evaluation_agent.py
Evaluates answers using AI

voice.py
Handles audio recording and transcription

resume_parser.py
Extracts skills, projects, and experience from resume

requirements.txt
Project dependencies

.env
API key (not tracked by Git)

.gitignore
Security configuration

README.md
Project documentation

---

# ⚙️ Installation

## 1. Clone the repository

git clone https://github.com/eshan202005/AI-Mock-Interviewer.git

cd AI-Mock-Interviewer

---

## 2. Create virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

---

## 3. Install dependencies

pip install -r requirements.txt

---

## 4. Create `.env` file

Create a file named:

.env

Add:

GROQ_API_KEY=your_api_key_here

---

## 5. Run the application

streamlit run app.py

---

# 🧪 Example Workflow

1. Enter your name
2. Select interview role
3. Upload resume
4. Click "Process Resume"
5. Answer questions (voice or text)
6. Receive evaluation and feedback

---

# 🔒 Security

This project follows secure API handling practices:

* API keys stored in `.env`
* `.env` excluded via `.gitignore`
* No secrets committed to GitHub

---

# 📈 Current Capabilities

* Resume parsing
* Personalized question generation
* Voice recording
* Speech transcription
* Automated evaluation
* Session state tracking
* Secure environment configuration
* GitHub version control

---

# 🔮 Planned Improvements

* Interview timer
* Progress bar
* Score dashboard
* Performance analytics
* Deployment (Streamlit Cloud / Render)
* UI enhancements

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

* Python application development
* Streamlit UI design
* Session state management
* API integration
* Prompt engineering
* Secure environment configuration
* Git version control
* Modular software architecture

---

# 👨‍💻 Author

Eshan Gupta

Computer Science Student
Aspiring Data Scientist / Software Engineer

---

# ⭐ If you find this project useful

Consider starring the repository.
