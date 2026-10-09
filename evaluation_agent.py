from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def evaluate_answer(question, answer, question_number):

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"))

    # Check if answer is empty or just whitespace
    if not answer or answer.strip() == "" or len(answer.strip()) < 5:
        if question_number < 2:  # Coding questions
            return "Result: Not Attempted\nScore: 0/10\nFeedback: No code was provided.\nImprovement: Write code to solve the problem."
        else:  # Non-coding questions
            return "Result: Not Attempted\nFeedback: No response was provided.\nImprovement: Provide a detailed answer."

    prompt = f"""
You are an expert technical interviewer.

IMPORTANT RULE:

- Question 1 and Question 2 are coding questions.
- All remaining questions are non-coding questions.

--------------------------------

CODING QUESTIONS:

Evaluate the candidate's code.

Provide:
Result: Correct or Incorrect
Score: X/10
Logic Feedback: Explain where the logic is right or wrong
Improvement: Suggest one improvement

--------------------------------

NON-CODING QUESTIONS:

First decide: Is the answer correct or incorrect?

Rules:

- If the answer is completely wrong or irrelevant:
    Result: Incorrect
    Do NOT give a score

- If the answer is partially correct or correct:
    Result: Correct
    Score: X/10
    Feedback: Brief evaluation
    Improvement: How the candidate can improve

--------------------------------

Now evaluate:

Question Number: {question_number + 1}

Question:
{question}

Answer:
{answer}

Return in clean structured format.
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

    return response.choices[0].message.content
