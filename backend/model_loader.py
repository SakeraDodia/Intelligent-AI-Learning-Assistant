import torch
from pathlib import Path

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

from peft import PeftModel


# ============================================================
# PATHS
# ============================================================

# backend/
#     model_loader.py
#
# Project root:
#     ../
#
# LoRA adapter:
#     qwen-qlora-finetuning/outputs/qwen2.5-7b-qlora/

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent

ADAPTER_PATH = (
    PROJECT_DIR
    / "qwen-qlora-finetuning"
    / "outputs"
    / "qwen2.5-7b-qlora"
)


# ============================================================
# MODEL
# ============================================================

BASE_MODEL = "Qwen/Qwen2.5-7B-Instruct"


def load_model():

    print("=" * 60)
    print("Loading Qwen fine-tuned model...")
    print("=" * 60)

    print(f"Base model: {BASE_MODEL}")
    print(f"LoRA adapter: {ADAPTER_PATH}")

    # --------------------------------------------------------
    # Check adapter
    # --------------------------------------------------------

    if not ADAPTER_PATH.exists():

        raise FileNotFoundError(
            f"LoRA adapter not found at:\n{ADAPTER_PATH}"
        )

    # --------------------------------------------------------
    # Tokenizer
    # --------------------------------------------------------

    print("\nLoading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    tokenizer.padding_side = "left"

    # --------------------------------------------------------
    # 4-bit QLoRA configuration
    # --------------------------------------------------------

    print("\nCreating 4-bit quantization configuration...")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )

    # --------------------------------------------------------
    # Load base model
    # --------------------------------------------------------

    print("\nLoading base model...")

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        dtype=torch.float16,
        trust_remote_code=True
    )

    # --------------------------------------------------------
    # Load LoRA adapter
    # --------------------------------------------------------

    print("\nLoading QLoRA adapter...")

    model = PeftModel.from_pretrained(
        base_model,
        str(ADAPTER_PATH)
    )

    model.eval()

    print("\n" + "=" * 60)
    print("Fine-tuned model loaded successfully!")
    print("=" * 60)

    if torch.cuda.is_available():

        print(f"GPU: {torch.cuda.get_device_name(0)}")

        memory = torch.cuda.memory_allocated(0) / 1024**3

        print(f"GPU memory allocated: {memory:.2f} GB")

    return model, tokenizer