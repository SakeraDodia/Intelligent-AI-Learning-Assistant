from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Quiz Generator.

Generate useful quiz questions for AI/ML learners.

Questions should match the requested topic and difficulty.

Provide:
- Question
- Four options
- Correct answer
- Short explanation

Do not add unnecessary information.
"""


def generate_quiz(
    topic: str,
    difficulty: str = "medium",
    number_of_questions: int = 5
):

    prompt = f"""
Generate {number_of_questions} quiz questions.

Topic:
{topic}

Difficulty:
{difficulty}

Format each question clearly.
"""

    return generate_response(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        max_new_tokens=1200
    )