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
"""


def roadmap():

    print("\n========================================")
    print("         LEARNING ROADMAP")
    print("========================================")


    topic = input(
        "\nWhat do you want to learn? "
    )


    current_level = input(
        "What is your current level "
        "(beginner/intermediate/advanced)? "
    )


    study_time = input(
        "How much time can you study per day? "
    )


    duration = input(
        "How many weeks/months do you have? "
    )


    print("\nGenerating roadmap...\n")


    user_prompt = f"""
Create a personalized learning roadmap.

Topic:
{topic}

Current level:
{current_level}

Study time per day:
{study_time}

Available duration:
{duration}

Structure the roadmap as:

1. Prerequisites
2. Phase 1
3. Phase 2
4. Phase 3
5. Advanced topics
6. Practical projects
7. Practice/revision
8. Final project

Explain what should be learned in each phase.

Make the roadmap realistic and easy to follow.
"""


    response = generate_response(
        SYSTEM_PROMPT,
        user_prompt,
        max_new_tokens=1500
    )


    print("Assistant:")
    print(response)


if __name__ == "__main__":

    roadmap()