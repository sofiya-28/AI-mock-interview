from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()


def generate_questions(role, skills, projects, experience):

    
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"))

    
    has_experience = len(experience) > 0

    if has_experience:
        question_count = 15
    else:
        question_count = 12



    prompt = f"""
You are an expert technical interviewer.

Role: {role}

Skills: {skills}

Projects: {projects}

Experience: {experience}

Generate exactly {question_count} interview questions.

IMPORTANT — Follow this exact order:

1. Question 1 — DSA Coding Question (Easy)

2. Question 2 — DSA Coding Question (Medium)

These two coding questions MUST be LeetCode-style problems including:

- Problem statement
- Input
- Output
- Constraints

3–6 — Skill-based questions  
These must be based on the candidate's skills.

7–10 — Project-based questions  
These must be based on the candidate's projects.
"""

    if has_experience:

        prompt += """

11–13 — Experience-based questions  
These must be based on the candidate's work experience.

14–15 — HR questions
"""

    else:

        prompt += """

11–12 — HR questions
"""

    prompt += """

CRITICAL RULES:

- Generate EXACTLY the required number of questions
- Do NOT generate questions for both scenarios
- Do NOT print instructions
- Only return numbered questions
- The first two questions MUST be Data Structures and Algorithms coding problems'
= very important rule leaving question 1 and 2 all should be non coding questions

Return only numbered questions.
"""

    

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    
    questions_text = response.choices[0].message.content

    

    lines = questions_text.split("\n")

    questions = []
    current_question = ""

    for line in lines:

        line = line.strip()

        if not line:
            continue

        

        if line[0].isdigit() and "." in line:

            if current_question:
                questions.append(current_question.strip())

            current_question = line

        else:

            current_question += " " + line

    

    if current_question:
        questions.append(current_question.strip())

    

    questions = questions[:question_count]

    return questions