import re
from inference import generate_response


# ============================================================
# Generate ONE NEW INTERVIEW QUESTION
# ============================================================

def generate_interview_question(
    topic,
    difficulty,
    question_number,
    previous_questions
):

    if previous_questions:
        previous_text = "\n".join(
            f"- {q}" for q in previous_questions
        )
    else:
        previous_text = "None"

    prompt = f"""
You are a professional AI/ML interview coach.

Generate EXACTLY ONE interview question.

Interview topic:
{topic}

Difficulty:
{difficulty}

Question number:
{question_number}

Previously asked questions:
{previous_text}

STRICT RULES:

1. Generate exactly ONE interview question.
2. The new question MUST be different from every question
   in the previously asked list.
3. Do NOT repeat the same question using different wording.
4. Do NOT provide the answer.
5. Do NOT provide feedback.
6. Do NOT provide an explanation.
7. Do NOT generate multiple questions.
8. Do NOT number additional questions.
9. Ask a question directly related to the topic.
10. Match the requested difficulty.

Return ONLY:

Question {question_number}: <question>
"""

    response = generate_response(
        prompt,
        max_new_tokens=180
    )

    return clean_question(
        response,
        question_number
    )


# ============================================================
# Clean model output
# ============================================================

def clean_question(response, question_number):

    response = response.strip()

    # Remove everything after accidental second question
    response = re.split(
        r"\n\s*(?:Question\s*\d+[:.]|Q\d+[:.])",
        response,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    # Remove accidental answer/feedback
    response = re.split(
        r"\n\s*(?:Answer|Correct Answer|Explanation|Feedback)[:.]?",
        response,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    response = response.strip()

    # Remove duplicate "Question X:" if model generated it
    response = re.sub(
        r"^Question\s*\d+\s*:\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    return f"Question {question_number}: {response}"


# ============================================================
# Normalize question for duplicate checking
# ============================================================

def normalize_question(question):

    question = question.lower()

    # Remove question number
    question = re.sub(
        r"question\s*\d+\s*:",
        "",
        question
    )

    # Remove punctuation
    question = re.sub(
        r"[^a-z0-9\s]",
        "",
        question
    )

    # Remove extra spaces
    question = re.sub(
        r"\s+",
        " ",
        question
    )

    return question.strip()


# ============================================================
# Check whether question is duplicate
# ============================================================

def is_duplicate_question(
    new_question,
    previous_questions
):

    new_normalized = normalize_question(
        new_question
    )

    for old_question in previous_questions:

        old_normalized = normalize_question(
            old_question
        )

        # Exact duplicate
        if new_normalized == old_normalized:
            return True

        # If one question contains the other
        if (
            new_normalized in old_normalized
            or old_normalized in new_normalized
        ):
            return True

    return False


# ============================================================
# Generate question with duplicate protection
# ============================================================

def get_unique_question(
    topic,
    difficulty,
    question_number,
    previous_questions
):

    max_attempts = 5

    for attempt in range(max_attempts):

        question = generate_interview_question(
            topic=topic,
            difficulty=difficulty,
            question_number=question_number,
            previous_questions=previous_questions
        )

        if not is_duplicate_question(
            question,
            previous_questions
        ):
            return question

        print(
            "\n[Model generated a duplicate. "
            "Generating another question...]\n"
        )

    # If model repeatedly generates duplicates,
    # ask it with a stronger instruction.

    previous_text = "\n".join(
        f"- {q}" for q in previous_questions
    )

    emergency_prompt = f"""
Generate ONE completely different interview question.

Topic: {topic}
Difficulty: {difficulty}

DO NOT ask anything similar to these:

{previous_text}

You MUST ask about a different concept.

Return ONLY the question.
Do not provide an answer.
Do not provide explanation.
Do not generate another question.
"""

    question = generate_response(
        emergency_prompt,
        max_new_tokens=150
    )

    question = question.strip()

    return f"Question {question_number}: {question}"


# ============================================================
# Evaluate interview answer
# ============================================================

def evaluate_answer(
    topic,
    question,
    user_answer
):

    prompt = f"""
You are an AI/ML interview evaluator.

Topic:
{topic}

Interview question:
{question}

Candidate answer:
{user_answer}

Evaluate the candidate's answer.

Rules:

1. Determine whether the answer is correct.
2. Identify important missing points.
3. Give honest but concise feedback.
4. Do not ask another question.
5. Do not generate a new interview question.
6. Do not repeat the original question.

Return exactly:

RESULT: <Correct / Partially Correct / Incorrect>

FEEDBACK:
<brief feedback>

MODEL ANSWER:
<short ideal answer>
"""

    response = generate_response(
        prompt,
        max_new_tokens=300
    )

    return response.strip()


# ============================================================
# Get user answer
# ============================================================

def get_user_answer():

    print("\nYour answer:")

    answer = input("> ").strip()

    if answer.lower() == "exit":
        return "exit"

    return answer


# ============================================================
# Interview
# ============================================================

def interview():

    print("\n" + "=" * 55)
    print("                 INTERVIEW PREPARATION")
    print("=" * 55)

    topic = input(
        "\nEnter interview topic: "
    ).strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    while True:

        difficulty = input(
            "Enter difficulty "
            "(beginner/intermediate/advanced): "
        ).strip().lower()

        if difficulty in [
            "beginner",
            "intermediate",
            "advanced"
        ]:
            break

        print(
            "Please enter beginner, intermediate, "
            "or advanced."
        )

    while True:

        try:

            total_questions = int(
                input("How many questions? ").strip()
            )

            if total_questions > 0:
                break

            print("Enter a number greater than 0.")

        except ValueError:

            print("Please enter a valid number.")

    print("\nStarting interview...")
    print("-" * 55)

    # This list is VERY important.
    # It stores every question already asked.
    previous_questions = []

    for question_number in range(
        1,
        total_questions + 1
    ):

        # ----------------------------------------------------
        # Generate UNIQUE question
        # ----------------------------------------------------

        question = get_unique_question(
            topic=topic,
            difficulty=difficulty,
            question_number=question_number,
            previous_questions=previous_questions
        )

        # Store question BEFORE asking the user
        previous_questions.append(question)

        # ----------------------------------------------------
        # Display question
        # ----------------------------------------------------

        print("\nAssistant:")
        print(question)

        # ----------------------------------------------------
        # Get candidate answer
        # ----------------------------------------------------

        user_answer = get_user_answer()

        if user_answer == "exit":

            print("\nInterview ended.")
            break

        # ----------------------------------------------------
        # Evaluate answer
        # ----------------------------------------------------

        print("\nAssistant:")

        feedback = evaluate_answer(
            topic=topic,
            question=question,
            user_answer=user_answer
        )

        print(feedback)

        # ----------------------------------------------------
        # Next question
        # ----------------------------------------------------

        if question_number < total_questions:

            print("\n" + "-" * 55)

    print("\n" + "=" * 55)
    print("              INTERVIEW COMPLETED")
    print("=" * 55)


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    interview()