from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Learning Roadmap Assistant.

Create personalized and structured learning roadmaps.

Rules:

1. Understand what the user wants to learn.
2. Consider the user's current level.
3. Start with prerequisites.
4. Progress from beginner to advanced.
5. Organize topics into logical phases.
6. Include important subtopics.
7. Explain the recommended learning order.
8. Include practical projects.
9. Include practice recommendations.
10. Avoid unnecessary unrelated topics.
11. Make the roadmap practical for AI/ML learners.
12. Strictly respect the user's available duration.
13. Adapt the roadmap to the user's study time.
14. Prioritize essential topics.
"""


def generate_roadmap(
    topic: str,
    current_level: str,
    study_time: str,
    duration: str
):

    prompt = f"""
Create a personalized learning roadmap.

Topic:
{topic}

Current Level:
{current_level}

Study Time Per Day:
{study_time}

Available Duration:
{duration}

Structure the roadmap as:

1. Learning Goal
2. Prerequisites
3. Roadmap Overview
4. Phase/Week-wise Plan
5. Important Subtopics
6. Practice
7. Mini Projects
8. Advanced Topics
9. Revision
10. Final Project

Make the roadmap realistic and fit it within the
available duration.
"""

    return generate_response(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        max_new_tokens=1500
    )