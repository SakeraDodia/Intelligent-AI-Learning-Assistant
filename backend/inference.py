import torch

from model_loader import load_model


# ============================================================
# LOAD MODEL ONCE
# ============================================================

print("\nInitializing model...")

model, tokenizer = load_model()

print("Inference system ready!\n")


# ============================================================
# GENERATE RESPONSE
# ============================================================

def generate_response(
    prompt,
    system_prompt=None,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1
):
    """
    Generate a response using the fine-tuned Qwen + LoRA model.
    """

    # --------------------------------------------------------
    # Build chat messages
    # --------------------------------------------------------

    messages = []

    if system_prompt:

        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    # --------------------------------------------------------
    # Apply Qwen chat template
    # --------------------------------------------------------

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # --------------------------------------------------------
    # Tokenize
    # --------------------------------------------------------

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True
    )

    # --------------------------------------------------------
    # Move inputs to model device
    # --------------------------------------------------------

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    # --------------------------------------------------------
    # Generate
    # --------------------------------------------------------

    with torch.no_grad():

        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],

            max_new_tokens=max_new_tokens,

            temperature=temperature,
            top_p=top_p,

            do_sample=True,

            repetition_penalty=repetition_penalty,

            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    # --------------------------------------------------------
    # Remove input tokens
    # --------------------------------------------------------

    input_length = inputs["input_ids"].shape[-1]

    generated_tokens = outputs[0][input_length:]

    # --------------------------------------------------------
    # Decode
    # --------------------------------------------------------

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response.strip()