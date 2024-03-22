from llama_index.core.chat_engine.types import ChatMode

from src.pydantic_models.chat_models import ChatRequest
import src.rag.utils.create_settings
from src.rag.indexes.create_index import create_custom_index
from src.rag.inference.postprocessors.similarity import get_similarity_filter
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
import time


chat_store = SimpleChatStore()
index = create_custom_index(collection_name='html_parser')
similarity_filter = get_similarity_filter(threshold=0.4)


def ask_question(request: ChatRequest):

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=48000,
        chat_store=chat_store,
        chat_store_key=request.user_id + "_" + request.conversation_id,
    )
    start_time = time.time()
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        memory=chat_memory,
        context_prompt=
            """You are a kind and useful chatbot designed for Canton St. Gallen, tasked with responding to citizens' inquiries over the phone. Your goal is to assist citizens by leveraging specific documents to provide short, concise, and accurate answers. When faced with questions that extend beyond your knowledge base, or when a citizen requires additional support, your duty is to consult the documents to provide the contact number and email of the media and communication officer responsible for the relevant topic.

Here are the relevant documents for the context:
{context_str}

Instruction: Use the information within the provided documents to offer concise and direct answers to users' queries, ensuring your responses do not exceed four lines. When a query falls outside of your direct knowledge or requires further assistance, guide the user to the appropriate contact for media and communication. Remember to adapt your language to match the user's, paying special attention to maintaining high linguistic quality, particularly for questions posed in Swiss German dialects. Your primary aim is to serve the citizens of Canton St. Gallen with reliable information and clear guidance.""",
        similarity_top_k=5,
        # node_postprocessors=[similarity_filter]
    )

    response = chat_engine.chat(request.question)

    end_time = time.time()
    print("time to generate the answer backend:", end_time-start_time)
    return response
