import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import PeftModel


# =====================================================
# CONFIG
# =====================================================

BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"

LORA_PATH = "../outputs/qwen-learning-assistant"


# =====================================================
# TOKENIZER
# =====================================================

print("Loading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL,
    trust_remote_code=True,
)

tokenizer.pad_token = tokenizer.eos_token


# =====================================================
# LOAD BASE MODEL
# =====================================================

print("Loading Base Model...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)


# =====================================================
# LOAD LORA ADAPTER
# =====================================================

print("Loading LoRA Adapter...")

model = PeftModel.from_pretrained(
    model,
    LORA_PATH,
)

model.eval()

print("\n AI Learning Assistant is Ready!")
print("Type 'exit' to quit.\n")


# =====================================================
# CHAT LOOP
# =====================================================

while True:

    question = input("You : ").strip()

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    messages = [
        {
            "role": "system",
            "content": (
                "You are an Intelligent AI Learning Assistant. "
                "Help users learn Artificial Intelligence, Machine Learning, "
                "Deep Learning, Python, Data Science, NLP, Generative AI, "
                "Large Language Models, LangChain, PyTorch, TensorFlow, "
                "Transformers, RAG, Interview Preparation, Roadmaps, "
                "Quiz Generation, and PDF-based learning. "
                "Always explain concepts in a beginner-friendly way with "
                "examples whenever possible."
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(model.device)

    with torch.inference_mode():

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            repetition_penalty=1.1,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )

    print("\nAssistant:\n")
    print(response)
    print("\n" + "=" * 80 + "\n")