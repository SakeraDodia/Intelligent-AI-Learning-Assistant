from inference import generate_response


SYSTEM_PROMPT = """
You are an AI quiz generator for an AI/ML learning assistant.

Generate multiple-choice quizzes.

Each question must contain:

- Question
- Option A
- Option B
- Option C
- Option D
- Correct answer
- Short explanation

Questions must be clear and unambiguous.
"""


print("=" * 60)
print("QUIZ GENERATION TEST")
print("=" * 60)


user_prompt = """
Create 5 multiple-choice questions about Python functions.

Difficulty:
Beginner to intermediate.

Target:
AI/ML students.
"""


response = generate_response(
    SYSTEM_PROMPT,
    user_prompt,
    max_new_tokens=800
)


print("\nMODEL RESPONSE:\n")
print(response)