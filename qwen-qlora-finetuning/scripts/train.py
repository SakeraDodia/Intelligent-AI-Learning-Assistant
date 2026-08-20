import torch

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

from peft import LoraConfig

from trl import (
    SFTTrainer,
    SFTConfig
)


# ============================================================
# 1. CONFIG
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
DATASET = "./datasets/datasets.jsonl"
OUTPUT_DIR = "./outputs/qwen2.5-7b-qlora"


# ============================================================
# 2. LOAD DATASET
# ============================================================

dataset = load_dataset(
    "json",
    data_files=DATASET
)

dataset = dataset["train"].train_test_split(
    test_size=0.1,
    seed=42
)

train_dataset = dataset["train"]
eval_dataset = dataset["test"]


# ============================================================
# 3. LOAD TOKENIZER
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"


# ============================================================
# 4. APPLY CHAT TEMPLATE
# ============================================================

def format_chat(example):

    return {
        "text": tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False
        )
    }


train_dataset = train_dataset.map(
    format_chat
)

eval_dataset = eval_dataset.map(
    format_chat
)


# ============================================================
# 5. 4-BIT QUANTIZATION
# ============================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)


# ============================================================
# 6. LOAD QWEN MODEL
# ============================================================

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)


# ============================================================
# 7. LORA / PEFT CONFIGURATION
# ============================================================

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj"
    ],
    bias="none",
    task_type="CAUSAL_LM"
)


# ============================================================
# 8. SFT CONFIGURATION
# ============================================================

sft_config = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=1,  
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=100,
    eval_strategy="steps",
    eval_steps=100,
    save_total_limit=2,
    max_length=2048,
    bf16=True,
    gradient_checkpointing=True,
    report_to="none"
)


# ============================================================
# 9. SFT TRAINER
# ============================================================

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
    args=sft_config
)


# ============================================================
# 10. CHECK TRAINABLE PARAMETERS
# ============================================================

trainer.model.print_trainable_parameters()


# ============================================================
# 11. TRAIN
# ============================================================

trainer.train()


# ============================================================
# 12. SAVE ADAPTER
# ============================================================

trainer.save_model(
    OUTPUT_DIR
)

tokenizer.save_pretrained(
    OUTPUT_DIR
)

print("Training completed!")
print(f"Adapter saved at: {OUTPUT_DIR}")