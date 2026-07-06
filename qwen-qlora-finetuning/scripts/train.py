import torch
from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
)

from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
)

from trl import SFTTrainer

# =====================================================
# Configuration
# =====================================================

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

DATASET_PATH = "../datasets/merged_sft_dataset.jsonl"

OUTPUT_DIR = "../outputs"

# =====================================================
# Load Dataset
# =====================================================

print("Loading Dataset...")

dataset = load_dataset(
    "json",
    data_files=DATASET_PATH,
    split="train"
)

print(dataset)

# =====================================================
# Load Tokenizer
# =====================================================

print("Loading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True
)

tokenizer.pad_token = tokenizer.eos_token

# =====================================================
# QLoRA Quantization
# =====================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# =====================================================
# Load Model
# =====================================================

print("Loading Qwen Model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

model.config.use_cache = False

model = prepare_model_for_kbit_training(model)

# =====================================================
# LoRA Configuration
# =====================================================

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)

model.print_trainable_parameters()

# =====================================================
# Training Arguments
# =====================================================

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    per_device_train_batch_size=1,

    gradient_accumulation_steps=8,

    learning_rate=2e-4,

    num_train_epochs=3,

    logging_steps=10,

    save_steps=200,

    save_total_limit=2,

    fp16=True,

    optim="paged_adamw_8bit",

    lr_scheduler_type="cosine",

    warmup_ratio=0.03,

    report_to="none",
)

# =====================================================
# Trainer
# =====================================================

trainer = SFTTrainer(
    model=model,

    train_dataset=dataset,

    args=training_args,

    tokenizer=tokenizer,
)

# =====================================================
# Start Training
# =====================================================

print("Starting Training...")

trainer.train()

# =====================================================
# Save Adapter
# =====================================================

trainer.model.save_pretrained("../outputs/lora_adapter")

tokenizer.save_pretrained("../outputs/lora_adapter")

print("Training Completed Successfully!")