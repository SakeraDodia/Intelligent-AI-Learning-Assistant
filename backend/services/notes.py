from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Notes Generator.

Create clear and structured study notes.

Include:

- Definition
- Key concepts
- Important points
- Examples
- Advantages/disadvantages when relevant
- Interview points

Make the notes easy to understand and revise.
"""


def generate_notes(
    topic: str,
    level: str = "beginner"
):

    prompt = f"""
Create study notes for:

Topic:
{topic}

Level:
{level}

Make the notes structured and useful for AI/ML learning
and interview preparation.
"""

    return generate_response(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        max_new_tokens=1200
    )