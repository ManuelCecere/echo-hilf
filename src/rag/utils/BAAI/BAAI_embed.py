from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def load_baai_embeddings():
        embed_model = HuggingFaceEmbedding(
                model_name='BAAI/bge-large-en-v1.5',
                device = 'cuda',
                normalize=True,
                query_instruction='Generate a representation for this sentence that can be used to retrieve related articles:'
                )
        return embed_model