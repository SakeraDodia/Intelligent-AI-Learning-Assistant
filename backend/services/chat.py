from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML Learning Assistant.

Help users understand Artificial Intelligence,
Machine Learning, Deep Learning, NLP, Transformers,
LLMs, Generative AI, RAG and Fine-tuning.

Give clear, accurate and easy-to-understand answers.

Use examples when helpful.
"""


def chat(message: str):

    return generate_response(
        prompt=message,
        system_prompt=SYSTEM_PROMPT,
        max_new_tokens=800
    )