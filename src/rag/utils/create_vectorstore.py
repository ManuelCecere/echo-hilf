from llama_index.vector_stores.chroma.base import ChromaVectorStore
import src.rag.utils.create_settings
from llama_index.core.settings import Settings
import chromadb


def get_or_create_collection(collection: str) -> ChromaVectorStore:
    db = chromadb.PersistentClient(path=Settings.persist_dir)
    return db.get_or_create_collection(name=collection, metadata={"hnsw:space": "cosine"})


def get_or_create_vs(collection: str) -> ChromaVectorStore:
    chroma_collection = get_or_create_collection(collection=collection)
    return ChromaVectorStore(collection_name=collection, chroma_collection=chroma_collection, persist_dir=f"{Settings.persist_dir}/{collection}")

