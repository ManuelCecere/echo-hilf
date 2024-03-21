from pathlib import Path

from llama_index.readers.file import FlatReader
from unstructured.chunking.title import chunk_by_title
from unstructured.documents.elements import CompositeElement

from src.rag.loaders.parsers import Document
from src.rag.loaders.unstruct import unstructured_html_loader
from src.utils.logger import setup_logger
from typing import List
import os

logger = setup_logger(__name__)


def html_batch_parser(paths: List[str] | str) -> List[Document]:

    documents = []
    alias = 7000

    def process_html_file(file_path: str, directory_path: str, alias: int, url: str =""):

        try:
            elements = unstructured_html_loader(dir_path=directory_path, path=file_path, url=url)

            chunks = chunk_by_title(elements, max_characters=2000)

            new_chunks = []
            for chunk in chunks:
                new_metadata = chunk.metadata.to_dict()
                for key in new_metadata:
                    if isinstance(new_metadata[key], list):
                        new_metadata[key] = " ".join([el if el is not None else "" for el in new_metadata[key]])
                new_chunks.append(Document(text=chunk.text, metadata=new_metadata))

            documents.extend(new_chunks)

            # `documents` now contains Document objects that can be used with lalama_index functionality

            logger.info(f"Processed {file_path}.")
        except Exception as e:
            print(e)
        return alias + 1

    def process_directory(directory_path: str, alias: int):
        # Process all PDF files in the directory and its subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.lower().endswith('.html'):
                    file_path = root + "/" + file
                    alias = process_html_file(file_path, directory_path, alias)
        return alias

    if isinstance(paths, str):
        if os.path.isfile(paths) and paths.lower().endswith('.html'):
            # Process single PDF file
            alias = process_html_file(paths, paths[:paths.rfind('/') + 1], alias)
        elif os.path.isdir(paths):
            # Process a single directory
            alias = process_directory(paths, alias)
    elif isinstance(paths, list):
        for path in paths:
            if os.path.isfile(path) and path.lower().endswith('.html'):
                alias = process_html_file(path, path[:path.rfind('/') + 1], alias)
            elif os.path.isdir(path):
                # Process each directory in the list
                alias = process_directory(path, alias)

    return documents

