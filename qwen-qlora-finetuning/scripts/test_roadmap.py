from inference import generate_response


SYSTEM_PROMPT = """
You are an AI/ML learning roadmap assistant.

Create structured learning roadmaps.

The roadmap must:

1. Start from prerequisites.
2. Progress from beginner to advanced.
3. Clearly order the topics.
4. Include important subtopics.
5. Explain what should be learned first.
6. Avoid unnecessary topics.
7. Be practical for someone preparing for an AI/ML career.
"""


print("=" * 60)
print("ROADMAP GENERATION TEST")
print("=" * 60)


user_prompt = """
Create a complete roadmap for becoming a
Generative AI / LLM Engineer.

Include:

Python
Machine Learning
Deep Learning
NLP
Transformers
LLMs
RAG
Fine-tuning
Deployment
"""


response = generate_response(
    SYSTEM_PROMPT,
    user_prompt,
    max_new_tokens=1200
)


print("\nMODEL RESPONSE:\n")
print(response)