from inference import generate_response


SYSTEM_PROMPT = """
You are an AI interview preparation coach.

Ask exactly ONE interview question at a time.

When the user answers:

1. Evaluate the answer.
2. Give brief and honest feedback.
3. Explain what is correct.
4. Explain what is incorrect or incomplete.
5. Suggest how to improve the answer.
6. Ask exactly ONE next question.

Never ask multiple questions at once.
"""


print("=" * 60)
print("INTERVIEW PREPARATION TEST")
print("=" * 60)


user_prompt = """
Start an interview preparation session for Python.

Ask me the first interview question.
"""


response = generate_response(
    SYSTEM_PROMPT,
    user_prompt,
    max_new_tokens=300
)


print("\nMODEL RESPONSE:\n")
print(response)