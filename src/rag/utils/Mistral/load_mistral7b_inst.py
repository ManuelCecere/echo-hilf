from llama_index.llms.huggingface import HuggingFaceLLM
import torch
from transformers import AutoTokenizer 



def load_llm(model = "mistralai/Mistral-7B-Instruct-v0.2"): 
    tokenizer = AutoTokenizer.from_pretrained(model)
    llm = HuggingFaceLLM (
            context_window = 8192, # 2048,
            max_new_tokens = 720, # 512, # 256,
            generate_kwargs = {"temperature": 0.1, "repetition_penalty": 1.1, "do_sample": True, 'pad_token_id': tokenizer.eos_token_id},
            query_wrapper_prompt = "{query_str}",
            model_name = model,
            device_map = "auto",
            tokenizer_kwargs = {"max_length": 4000},
            # uncomment this if using CUDA to reduce memory usage
            model_kwargs = {"torch_dtype": torch.bfloat16},
    )

    return llm