import re
from inference import generate_response


# ============================================================
# Generate ONE quiz question
# ============================================================

def generate_quiz_question(topic, difficulty, question_number, previous_questions):
    previous_text = "\n".join(
        f"- {q}" for q in previous_questions
    )

    prompt = f"""
You are a professional AI/ML quiz generator.

Generate EXACTLY ONE multiple-choice question.

Topic: {topic}
Difficulty: {difficulty}
Question number: {question_number}

Previously asked questions:
{previous_text if previous_text else "None"}

IMPORTANT RULES:
1. Generate exactly ONE question.
2. Do NOT repeat any previous question.
3. Do NOT provide the answer.
4. Do NOT provide an explanation.
5. Do NOT generate another question.
6. Give exactly four options: A, B, C, D.
7. Make only ONE option correct.
8. Keep the question relevant to the requested topic.
9. Return ONLY this format:

Question {question_number}: <question>

A. <option>
B. <option>
C. <option>
D. <option>
"""

    response = generate_response(
        prompt,
        max_new_tokens=250
    )

    return clean_question(response, question_number)


# ============================================================
# Clean generated question
# ============================================================

def clean_question(response, question_number):

    response = response.strip()

    # Remove accidental extra questions
    response = re.split(
        r"\n\s*(?:Question\s*\d+[:.]|Q\d+[:.])",
        response,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    # Remove unwanted answer/explanation sections
    response = re.split(
        r"\n\s*(?:Answer|Correct Answer|Explanation)[:.]?",
        response,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    response = response.strip()

    # If model forgot "Question X:"
    if not re.match(
        rf"^Question\s*{question_number}\s*:",
        response,
        re.IGNORECASE
    ):
        response = f"Question {question_number}: {response}"

    return response


# ============================================================
# Extract question text
# ============================================================

def extract_question_text(question):

    match = re.search(
        r"Question\s*\d+\s*:\s*(.*?)(?=\n\s*A[.)])",
        question,
        flags=re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return question.strip()


# ============================================================
# Extract options
# ============================================================

def extract_options(question):

    options = {}

    pattern = r"^\s*([ABCD])[.)]\s*(.+?)\s*$"

    for line in question.splitlines():

        match = re.match(
            pattern,
            line,
            flags=re.IGNORECASE
        )

        if match:
            letter = match.group(1).upper()
            text = match.group(2).strip()

            options[letter] = text

    return options


# ============================================================
# Evaluate answer
# ============================================================

def evaluate_answer(question, user_answer, topic):

    prompt = f"""
You are a quiz evaluator.

Topic: {topic}

Question:
{question}

User answer:
{user_answer}

Evaluate the user's answer.

IMPORTANT:
1. Determine whether the answer is correct.
2. If the user answered with A/B/C/D, compare it with the correct option.
3. If the user entered the option text, determine whether it matches the correct answer.
4. Give the correct answer.
5. Give a short explanation.
6. Do NOT generate another question.
7. Do NOT ask the user anything.

Return EXACTLY this format:

RESULT: Correct

CORRECT ANSWER: B

EXPLANATION: <short explanation>
"""

    response = generate_response(
        prompt,
        max_new_tokens=180
    )

    return response.strip()


# ============================================================
# Validate user's answer
# ============================================================

def get_user_answer():

    while True:

        answer = input(
            "\nYour answer (A/B/C/D or exit): "
        ).strip()

        if answer.lower() == "exit":
            return "exit"

        if answer.upper() in ["A", "B", "C", "D"]:
            return answer.upper()

        print("Please enter A, B, C, or D.")


# ============================================================
# Main Quiz
# ============================================================

def quiz():

    print("\n" + "=" * 50)
    print("                    QUIZ")
    print("=" * 50)

    topic = input("\nEnter quiz topic: ").strip()

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

    print("\nStarting quiz...")
    print("-" * 50)

    previous_questions = []

    score = 0

    for question_number in range(
        1,
        total_questions + 1
    ):

        # ----------------------------------------------------
        # Generate one NEW question
        # ----------------------------------------------------

        question = generate_quiz_question(
            topic=topic,
            difficulty=difficulty,
            question_number=question_number,
            previous_questions=previous_questions
        )

        # Save only the question text for duplicate prevention
        question_text = extract_question_text(question)

        previous_questions.append(question_text)

        # ----------------------------------------------------
        # Display question
        # ----------------------------------------------------

        print("\nAssistant:")
        print(question)

        # ----------------------------------------------------
        # Get user's answer
        # ----------------------------------------------------

        user_answer = get_user_answer()

        if user_answer == "exit":

            print("\nQuiz ended.")
            break

        # ----------------------------------------------------
        # Evaluate answer
        # ----------------------------------------------------

        print("\nAssistant:")

        evaluation = evaluate_answer(
            question=question,
            user_answer=user_answer,
            topic=topic
        )

        print(evaluation)

        # ----------------------------------------------------
        # Calculate score
        # ----------------------------------------------------

        if re.search(
            r"RESULT\s*:\s*Correct\b",
            evaluation,
            flags=re.IGNORECASE
        ):
            score += 1

        # ----------------------------------------------------
        # Separate questions
        # ----------------------------------------------------

        if question_number < total_questions:

            print("\n" + "-" * 50)

    # ========================================================
    # Final Score
    # ========================================================

    print("\n" + "=" * 50)
    print("                 QUIZ RESULT")
    print("=" * 50)

    print(
        f"\nScore: {score}/{total_questions}"
    )

    if total_questions > 0:

        percentage = (
            score / total_questions
        ) * 100

        print(
            f"Percentage: {percentage:.1f}%"
        )

    print("\nQuiz completed.")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    quiz()