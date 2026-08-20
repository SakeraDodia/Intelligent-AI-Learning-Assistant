import torch

from model_loader import load_model


# Load model only once
model, tokenizer = load_model()


def generate_response(
    system_prompt,
    user_prompt,
    max_new_tokens=500,
    temperature=0.7,
    top_p=0.9
):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


    # Convert messages into Qwen chat format
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )


    # Tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    )


    # Move inputs to GPU
    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }


    # Generate
    with torch.no_grad():

        outputs = model.generate(
            **inputs,

            max_new_tokens=max_new_tokens,

            temperature=temperature,

            top_p=top_p,

            do_sample=True,

            repetition_penalty=1.1,

            pad_token_id=tokenizer.pad_token_id,

            eos_token_id=tokenizer.eos_token_id
        )


    # Remove prompt tokens
    generated_tokens = outputs[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]


    # Decode
    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )


    return response.strip()