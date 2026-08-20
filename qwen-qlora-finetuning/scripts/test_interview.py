from inference import generate_response


SYSTEM_PROMPT = """
You are an AI Interview Preparation Coach.

Your job is to conduct an interactive interview preparation session.

Rules:

1. Ask exactly ONE interview question at a time.
2. Wait for the user's answer.
3. Evaluate the user's answer.
4. Tell the user what was correct.
5. Explain what is wrong or missing.
6. Give a short improvement suggestion.
7. Then ask exactly ONE next question.
8. Never ask multiple questions at once.
9. Questions must be related to the selected topic.
10. Start with basic questions and gradually increase difficulty.
11. Do not reveal the answer before the user attempts the question.
"""


def interview():

    print("\n========================================")
    print("       INTERVIEW PREPARATION")
    print("========================================")

    topic = input("\nEnter interview topic: ")

    difficulty = input(
        "Enter difficulty "
        "(beginner/intermediate/advanced): "
    )

    print("\nStarting interview...\n")


    conversation = []


    # ------------------------------------
    # FIRST QUESTION
    # ------------------------------------

    user_prompt = f"""
Start an interview preparation session.

Topic: {topic}

Difficulty: {difficulty}

Ask the FIRST interview question.

Ask exactly ONE question.
Do not provide the answer.
"""


    response = generate_response(
        SYSTEM_PROMPT,
        user_prompt,
        max_new_tokens=400
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
    # INTERVIEW LOOP
    # ------------------------------------

    while True:

        print("\n----------------------------------------")

        user_answer = input(
            "Your answer "
            "(type 'exit' to stop): "
        )


        if user_answer.lower() == "exit":

            print("\nInterview ended.")

            break


        conversation.append(
            {
                "role": "user",
                "content": user_answer
            }
        )


        # Build conversation history

        history = ""

        for message in conversation:

            history += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )


        user_prompt = f"""
Continue the interview.

Topic: {topic}

Difficulty: {difficulty}

Conversation so far:

{history}

The user has answered the latest interview question.

Now:

1. Evaluate the user's answer.
2. Tell what was correct.
3. Explain mistakes or missing information.
4. Give a short improvement suggestion.
5. Ask exactly ONE next interview question.

Do not ask multiple questions.
Do not give the answer before asking the next question.
"""


        response = generate_response(
            SYSTEM_PROMPT,
            user_prompt,
            max_new_tokens=500
        )


        print("\nAssistant:")
        print(response)


        conversation.append(
            {
                "role": "assistant",
                "content": response
            }
        )


if __name__ == "__main__":

    interview()