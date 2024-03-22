from unstructured.documents.elements import CompositeElement

from src.rag.loaders.ingestion_pipeline import create_html_pipeline
from src.utils.findPath import find_relative_path as fp
from src.rag.loaders.batch_parser import html_batch_parser
from llama_index.core.schema import BaseNode
from src.utils.logger import setup_logger
from typing import List


logger = setup_logger(__name__)


# define loader for scipdf_parser
def load_and_process(paths: List[str] | str, collection_name: str) -> List[BaseNode]:
    # create pipeline
    pipe = create_html_pipeline(collection_name=collection_name)

    docs = html_batch_parser(paths)

    # get nodes transformed as via the pipeline
    nodes = pipe.run(documents=docs)

    logger.info(f"Loaded {len(nodes)} nodes to collection {collection_name} from {len(docs)} documents.")

    # persist pipeline cache for faster utilization
    pipe.persist('./data/pipeline_storage')

    return nodes


if __name__ == '__main__':
    dirpath = "data/data/"

    nodes = load_and_process(dirpath, 'html_parsed')
    print("completed")
