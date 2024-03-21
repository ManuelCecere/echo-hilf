from llama_index.core.node_parser import SimpleNodeParser, NodeParser

import config.config_file
from src.rag.utils.create_vectorstore import get_or_create_vs
from llama_index.core.ingestion import IngestionPipeline
import src.rag.utils.create_settings
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def create_html_pipeline(collection_name: str) -> IngestionPipeline:
    # define vector store
    vector_store = get_or_create_vs(collection=collection_name)
    tags = [
        "p",  # Paragraphs
        "h1",  # Main headings
        "h2",  # Subheadings
        "h3",  # Sub-subheadings
        "h4",  # Further subheadings
        "h5",  # Even further subheadings
        "h6",  # Deepest level of subheadings
        "li",  # List items
        "ul",  # Unordered lists
        "ol",  # Ordered lists
        "dl",  # Description lists
        "dt",  # Terms in a description list
        "dd",  # Descriptions in a description list
        "blockquote",  # Block quotes
        "pre",  # Preformatted text
        "code",  # Code samples within text
        "a",  # Hyperlinks
        "strong",  # Strong emphasis
        "em",  # Emphasis
        "span",  # Inline container
        "div",  # Block-level container
        "table",  # Tables
        "thead",  # Table headings
        "tbody",  # Table body
        "tfoot",  # Table foot
        "tr",  # Table rows
        "th",  # Table header cells
        "td"  # Table data cells
    ]

    # parser = HTMLNodeParser(tags=["body"])  # optional list of tags
    parser = SimpleNodeParser()  # optional list of tags
    # define pipeline
    pipe = IngestionPipeline(
        transformations=[
            # *Settings.transformations,
            # parser,
            Settings.embed_model,
        ],
        vector_store=vector_store,
    )

    pipe.load(persist_dir='./data/pipeline_storage')

    return pipe
