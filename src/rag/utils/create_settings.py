import os

import openai
# from src.rag.utils.Sglang.sglang_loader import load_llm
# from src.rag.utils.gritLM.gritLM_loader import load_llm_embeddings
# from src.rag.utils.Mistral.load_mistral7b_inst import load_llm
# from src.rag.utils.BAAI.BAAI_embed import load_baai_embeddings
from llama_index.core.settings import Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.extractors import KeywordExtractor, QuestionsAnsweredExtractor
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.openai import OpenAI
from src.utils.logger import setup_logger
from llama_index.embeddings.cohere import CohereEmbedding
from dotenv import load_dotenv


load_dotenv("config/credentials.env")  # This loads the environment variables from .env
logger = setup_logger(__name__)
openai.api_key = os.environ["OPENAI_KEY"]


def initialize_settings():
    # here we load mistral v2 7b and baai large
    # Settings.llm = load_llm(max_tokens=2180)
    tokenizer = Anthropic().tokenizer
    Settings.tokenizer = tokenizer

    # Settings.llm = OpenAI("gpt-4-0125-preview", api_key=os.environ["OPENAI_KEY"])
    Settings.llm = OpenAI("gpt-4-turbo-preview", api_key=os.environ["OPENAI_KEY"])
    # Settings.llm = Anthropic(model="claude-3-haiku-20240307")

    # Settings.embed_model = load_baai_embeddings()

    # with input_typ='search_query'
    embed_model = CohereEmbedding(
        cohere_api_key=os.environ["COHERE_API_KEY"],
        model_name="embed-multilingual-v3.0",
        input_type="search_query",
    )

    Settings.embed_model = embed_model
    # load llm and embeddings from gritLM
    # Settings.llm, Settings.embed_model = load_llm_embeddings()

    # load node parser
    Settings.node_parser = SemanticSplitterNodeParser(buffer_size=3, breakpoint_percentile_threshold=95,
                                                      embed_model=Settings.embed_model)

    # # define extractors
    # Settings.transformations = [
    #     KeywordExtractor(keywords=5),
    #     QuestionsAnsweredExtractor(questions=2),
    # ]

    # vector store settings
    Settings.persist_dir = "./data/DBs"
    Settings.is_persistent = True

    logger.info("Settings initialized.")


initialize_settings()
