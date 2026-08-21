from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Interview Preparation Assistant.

Ask one interview question at a time.

Questions should be relevant to the requested topic
and difficulty level.

Start from basic concepts and gradually increase
the difficulty.

Do not provide the answer unless the user asks for it.
"""


def generate_interview_question(
    topic: str,
    level: str = "beginner",
    previous_questions: list[str] | None = None
):

    previous_questions = previous_questions or []

    previous_text = "\n".join(
        f"- {question}"
        for question in previous_questions
    )

    prompt = f"""
Generate ONE AI/ML interview question.

Topic:
{topic}

Level:
{level}

Previously asked questions:
{previous_text if previous_text else "None"}

Important:
- Do not repeat any previous question.
- Ask only ONE question.
- Do not provide the answer.
- Make the question appropriate for the level.
"""

    return generate_response(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        max_new_tokens=300
    )