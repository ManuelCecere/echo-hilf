from llama_index.core.chat_engine.types import ChatMode

from src.pydantic_models.chat_models import ChatRequest
import src.rag.utils.create_settings
from src.rag.indexes.create_index import create_custom_index
from src.rag.inference.postprocessors.similarity import get_similarity_filter
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
import time


chat_store = SimpleChatStore()
index = create_custom_index(collection_name='html_docs')
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
        context_prompt=(
            "You are a kind and useful chatbot for Canton St.Gallen, answering phone call from citizens. You must help citizens, "
            "using the following documents to provide a short, concise and completely sure answer. If you do not know "
            "the answer,"
            "or if a citizen asks for support, use the documents to return the contact number and email of the media "
            "and communication person responsible for that topic.\n"
            "\n\nHere are the relevant documents for the context:\n"
            "{context_str}"
            "\n\nInstruction: Based on the above documents, provide a concise and direct answer for the user, stay under 4 lines "
            "question below. Imagine to be"
        ),
        similarity_top_k=5,
        # node_postprocessors=[similarity_filter]
    )

    response = chat_engine.chat(request.question)
    # for token in response.response_gen:
    #     print(token, end="")

    # for r in response.source_nodes:
    #     print('Node similarity:', r.score)
    #     print('Section header:', r.metadata['section_heading'])
    #     print('Section imgs:', r.metadata['figures_refs']) if 'figures_refs' in r.metadata else print('No images')
    #     print('Section tabs:', r.metadata['tables_refs']) if 'tables_refs' in r.metadata else print('No tables')
    #     print('Section text:', r.text)
    #     print('---')

    # for r in response.source_nodes:
    #     print('Node similarity:', r.score)
    #     print('Section header:', r.metadata['section_heading'])
    #     print('Section imgs:', r.metadata['figures_refs']) if 'figures_refs' in r.metadata else print('No images')
    #     print('Section tabs:', r.metadata['tables_refs']) if 'tables_refs' in r.metadata else print('No tables')
    #     print('Section text:', r.text)
    #     print('---')
    end_time = time.time()
    print("time to generate the answer backend:", end_time-start_time)
    return response


def ask_question_stream(request: ChatRequest):
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=48000,
        chat_store=chat_store,
        chat_store_key=request.user_id + "_" + request.conversation_id,
    )
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        memory=chat_memory,
        context_prompt=(
            "You are a chatbot for Canton St.Gallen, answering phone call from citizens. You must help citizens, "
            "using the following documents to provide a short, concise and completely sure answer. If you do not know "
            "the answer,"
            "or if a citizen asks for support, use the documents to return the contact number and email of the media "
            "and communication person responsible for that topic.\n"
            "\n\nHere are the relevant documents for the context:\n"
            "{context_str}"
            "\n\nInstruction: Based on the above documents, provide a concise and direct answer for the user "
            "question below."
        ),
        similarity_top_k=5,
        # node_postprocessors=[similarity_filter]
    )

    response = chat_engine.chat(request.question)
    # for token in response.response_gen:
    #     print(token, end="")

    # for r in response.source_nodes:
    #     print('Node similarity:', r.score)
    #     print('Section header:', r.metadata['section_heading'])
    #     print('Section imgs:', r.metadata['figures_refs']) if 'figures_refs' in r.metadata else print('No images')
    #     print('Section tabs:', r.metadata['tables_refs']) if 'tables_refs' in r.metadata else print('No tables')
    #     print('Section text:', r.text)
    #     print('---')

    return response


def ask_question_stream(request: ChatRequest):
    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=48000,
        chat_store=chat_store,
        chat_store_key=request.user_id + "_" + request.conversation_id,
    )
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        memory=chat_memory,
        context_prompt=(
            "You are a chatbot for Canton St.Gallen, answering phone call from citizens. You must help citizens, "
            "using the following documents to provide a short, concise and completely sure answer. If you do not know "
            "the answer,"
            "or if a citizen asks for support, use the documents to return the contact number and email of the media "
            "and communication person responsible for that topic.\n"
            "\n\nHere are the relevant documents for the context:\n"
            "{context_str}"
            "\n\nInstruction: Based on the above documents, provide a concise and direct answer for the user "
            "question below."
        ),
        similarity_top_k=5,
        # node_postprocessors=[similarity_filter]
    )

    response = chat_engine.astream_chat(request.question)
    # for token in response.response_gen:
    #     print(token, end="")

    # for r in response.source_nodes:
    #     print('Node similarity:', r.score)
    #     print('Section header:', r.metadata['section_heading'])
    #     print('Section imgs:', r.metadata['figures_refs']) if 'figures_refs' in r.metadata else print('No images')
    #     print('Section tabs:', r.metadata['tables_refs']) if 'tables_refs' in r.metadata else print('No tables')
    #     print('Section text:', r.text)
    #     print('---')

    return response