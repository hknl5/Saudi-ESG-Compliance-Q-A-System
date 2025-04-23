import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_multiple_answers(question, top_chunks, num_versions=3):
    context = "\n\n".join(
        [f"Source ({chunk['source_file']}):\n{chunk['text']}" for chunk in top_chunks]
    )

    answers = []

    for i in range(num_versions):
        prompt = f"""
You are a compliance assistant AI. Based only on the provided text, answer the question below.
Do not invent or assume anything not stated in the text. Be accurate and grounded in the content.

Question:
{question}

Sources:
{context}

Answer version {i+1}:
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response["choices"][0]["message"]["content"].strip()
        answers.append(answer)

    return answers
def compare_answers(question, answer_list):
    all_answers_text = "\n\n".join([f"Answer {i+1}:\n{ans}" for i, ans in enumerate(answer_list)])

    prompt = f"""
You are a legal QA evaluator. Compare the following answers to the question: "{question}"
Identify the most accurate and clear answer based on the content. Justify your choice briefly.

{all_answers_text}

Which answer is best and why?
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]
