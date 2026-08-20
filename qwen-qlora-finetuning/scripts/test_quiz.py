from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Quiz Assistant.

Conduct an interactive quiz.

Rules:

1. Ask exactly ONE question at a time.
2. Each question must have four options:
   A
   B
   C
   D
3. Wait for the user's answer.
4. Check the user's answer.
5. Tell whether it is correct or incorrect.
6. Give the correct answer.
7. Give a short explanation.
8. Then ask exactly ONE next question.
9. Never ask multiple questions at once.
10. Questions must match the selected topic and difficulty.
11. Do not reveal the answer before the user answers.
"""


def quiz():

    print("\n========================================")
    print("              QUIZ")
    print("========================================")


    topic = input("\nEnter quiz topic: ")

    difficulty = input(
        "Enter difficulty "
        "(beginner/intermediate/advanced): "
    )

    total_questions = int(
        input("How many questions? ")
    )


    print("\nStarting quiz...\n")


    conversation = []

    question_number = 1


    # ------------------------------------
    # FIRST QUESTION
    # ------------------------------------

    user_prompt = f"""
Start a quiz.

Topic: {topic}

Difficulty: {difficulty}

Total questions: {total_questions}

Generate Question 1.

Format:

Question:
...

A. ...
B. ...
C. ...
D. ...

Do not give the answer.

Ask exactly ONE question.
"""


    response = generate_response(
        SYSTEM_PROMPT,
        user_prompt,
        max_new_tokens=500
    )


    print("Assistant:")
    print(response)


    conversation.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    # ------------------------------------
    # QUIZ LOOP
    # ------------------------------------

    while question_number <= total_questions:

        print("\n----------------------------------------")

        answer = input(
            "Your answer (A/B/C/D or exit): "
        )


        if answer.lower() == "exit":

            print("\nQuiz ended.")

            break


        conversation.append(
            {
                "role": "user",
                "content": answer
            }
        )


        history = ""

        for message in conversation:

            history += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )


        question_number += 1


        if question_number <= total_questions:

            next_question_instruction = f"""
After evaluating the user's answer,
ask Question {question_number}.

Ask exactly ONE question.

Do not reveal the answer before the user answers.
"""

        else:

            next_question_instruction = """
This was the final question.

Do not ask another question.

Give the final quiz result and a short summary.
"""


        user_prompt = f"""
Continue the quiz.

Topic: {topic}

Difficulty: {difficulty}

Total questions: {total_questions}

Conversation so far:

{history}

The user has just submitted an answer.

Now:

1. Check the answer.
2. Say whether it is correct or incorrect.
3. Give the correct answer.
4. Give a short explanation.

{next_question_instruction}
"""


        response = generate_response(
            SYSTEM_PROMPT,
            user_prompt,
            max_new_tokens=600
        )


        print("\nAssistant:")
        print(response)


        conversation.append(
            {
                "role": "assistant",
                "content": response
            }
        )


        if question_number > total_questions:

            break


if __name__ == "__main__":

    quiz()