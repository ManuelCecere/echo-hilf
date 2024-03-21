from src.rag.utils.create_vectorstore import get_or_create_vs
from llama_index.core import VectorStoreIndex
from llama_index.core.settings import Settings
from typing import List


def create_custom_index(collection_name: str) -> VectorStoreIndex:

    vector_store = get_or_create_vs(collection=collection_name)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model,
    )

    return index

