from gritlm import GritLM
from typing import Optional
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def load_grit():
    return GritLM("GritLM/GritLM-7B", device_map = 'auto', torch_dtype = 'auto')

   
def load_llm(gritlm: any):

    if gritlm is None:
        gritlm = load_grit() 

    grit_llm = HuggingFaceLLM(
        model           = gritlm.model, 
        tokenizer       = gritlm.tokenizer, 
        max_new_tokens  = 2000,
        context_window  = 8000,
        generate_kwargs ={
            'pad_token_id': gritlm.tokenizer.eos_token_id,  
            'temperature': 0.7, 
            'do_sample': True,
            }, 
        )

    return grit_llm

def load_embeddings(gritlm: any):

    if gritlm is None:
        gritlm =  load_grit()

    grit_embeddings = HuggingFaceEmbedding(
        model=gritlm.model, 
        tokenizer=gritlm.tokenizer,
        device=gritlm.device,
        text_instruction="<|embed|>\n",
        query_instruction="<|embed|>\n", 
        )

    return grit_embeddings

def load_llm_embeddings(gritlm: Optional[GritLM] = None):

    if gritlm is None:
        gritlm = load_grit()

    grit_embeddings = load_embeddings(gritlm) 
    grit_llm = load_llm(gritlm) 

    return grit_llm, grit_embeddings


if __name__ == "__main__":
    gritlm = GritLM("GritLM/GritLM-7B", device_map = 'auto', torch_dtype = 'auto')
    grit_llm, grit_embeddings = load_llm_embeddings(gritlm)
    mr_embeds = grit_embeddings.get_query_embedding("Who is Mark Ruffalo?")
    mr_answer = grit_llm.complete("Who is Mark Ruffalo?")
    print(mr_answer)
    