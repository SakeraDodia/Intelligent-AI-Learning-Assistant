import torch


# =====================================================
# RTX 3090 OPTIMIZATION
# =====================================================

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True



from datasets import load_dataset, concatenate_datasets


from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)


from peft import (
    LoraConfig,
    prepare_model_for_kbit_training,
    get_peft_model,
)


from trl import SFTTrainer, SFTConfig




# =====================================================
# CONFIG
# =====================================================


MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"


OUTPUT_DIR = "../outputs/qwen-learning-assistant"





# =====================================================
# DATASET FILES
# =====================================================


DATASET_FILES = [

    "../datasets/ai_chat.jsonl",

    "../datasets/interview.jsonl",

    "../datasets/notes.jsonl",

    "../datasets/pdf_chat.jsonl",

    "../datasets/quiz.jsonl",

    "../datasets/roadmap.jsonl"

]





# =====================================================
# LOAD ALL DATASETS
# =====================================================


print("="*60)
print("Loading All Datasets")
print("="*60)



dataset_list = []



for file in DATASET_FILES:


    print("Loading:", file)



    data = load_dataset(

        "json",

        data_files=file,

        split="train"

    )


    print("Samples:", len(data))


    dataset_list.append(data)





# Merge datasets


dataset = concatenate_datasets(

    dataset_list

)



print("="*60)

print("Combined Dataset")

print(dataset)

print("="*60)





# Train validation split


dataset = dataset.train_test_split(

    test_size=0.05,

    seed=42

)



train_dataset = dataset["train"]

eval_dataset = dataset["test"]



print("Training samples:", len(train_dataset))

print("Validation samples:", len(eval_dataset))





# =====================================================
# TOKENIZER
# =====================================================


print("="*60)

print("Loading Tokenizer")

print("="*60)



tokenizer = AutoTokenizer.from_pretrained(

    MODEL_NAME,

    trust_remote_code=True

)



tokenizer.pad_token = tokenizer.eos_token


tokenizer.padding_side = "right"





# =====================================================
# QLORA 4 BIT CONFIG
# =====================================================


bnb_config = BitsAndBytesConfig(


    load_in_4bit=True,


    bnb_4bit_quant_type="nf4",


    bnb_4bit_compute_dtype=torch.float16,


    bnb_4bit_use_double_quant=True

)





# =====================================================
# LOAD QWEN MODEL
# =====================================================


print("="*60)

print("Loading Model")

print("="*60)



model = AutoModelForCausalLM.from_pretrained(


    MODEL_NAME,


    quantization_config=bnb_config,


    device_map="auto",


    trust_remote_code=True

)




model.config.use_cache = False



model.gradient_checkpointing_enable()



model = prepare_model_for_kbit_training(

    model

)





# =====================================================
# LORA CONFIG
# =====================================================


peft_config = LoraConfig(


    r=16,


    lora_alpha=32,


    lora_dropout=0.05,


    bias="none",


    task_type="CAUSAL_LM",



    target_modules=[

        "q_proj",

        "k_proj",

        "v_proj",

        "o_proj",

        "gate_proj",

        "up_proj",

        "down_proj"

    ]

)



model = get_peft_model(

    model,

    peft_config

)



model.print_trainable_parameters()





# =====================================================
# TRAINING CONFIG
# =====================================================


training_args = SFTConfig(


    output_dir=OUTPUT_DIR,



    dataset_text_field="text",



    max_seq_length=2048,



    dataset_num_proc=8,



    packing=True,



    per_device_train_batch_size=2,



    gradient_accumulation_steps=4,



    learning_rate=2e-4,



    num_train_epochs=3,



    logging_steps=10,



    save_steps=200,



    save_total_limit=2,



    fp16=True,



    bf16=False,



    optim="paged_adamw_8bit",



    lr_scheduler_type="cosine",



    warmup_steps=100,



    group_by_length=True,



    dataloader_num_workers=4,



    report_to="none"

)






# =====================================================
# SFT TRAINER
# =====================================================


trainer = SFTTrainer(


    model=model,


    args=training_args,


    train_dataset=train_dataset,


    eval_dataset=eval_dataset,


    processing_class=tokenizer

)





# =====================================================
# START TRAINING
# =====================================================


print("="*60)

print("TRAINING STARTED")

print("="*60)



trainer.train()





# =====================================================
# SAVE LORA ADAPTER
# =====================================================


print("="*60)

print("Saving Model")

print("="*60)



trainer.model.save_pretrained(

    OUTPUT_DIR

)



tokenizer.save_pretrained(

    OUTPUT_DIR

)



print("="*60)

print("TRAINING COMPLETED SUCCESSFULLY")

print("="*60)