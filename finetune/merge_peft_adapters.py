from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_model_name_or_path", type=str, default="bigcode/large-model")
    parser.add_argument("--peft_model_path", type=str, default="/")
    parser.add_argument("--push_to_hub", action="store_true", default=True)
    parser.add_argument("--output_dir", type=str)

    return parser.parse_args()

def main():
    args = get_args()

    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model_name_or_path,
        return_dict=True,
        torch_dtype=torch.float16 
    )

    model = PeftModel.from_pretrained(base_model, args.peft_model_path)
    model = model.merge_and_unload()

    tokenizer = AutoTokenizer.from_pretrained(args.base_model_name_or_path)

    if args.push_to_hub:
        print(f"Saving to hub ...")
        model.push_to_hub(f"{args.output_dir}-merged", use_temp_dir=False, private=True)
        tokenizer.push_to_hub(f"{args.output_dir}-merged", use_temp_dir=False, private=True)
    else:
        model.save_pretrained(f"{args.output_dir}-merged")
        tokenizer.save_pretrained(f"{args.output_dir}-merged")
        print(f"Model saved to {args.output_dir}-merged")

if __name__ == "__main__" :
    main()
