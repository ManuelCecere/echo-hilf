from llama_index.core.postprocessor import SimilarityPostprocessor

threshold = 0.5


def get_similarity_filter(threshold: float = 0.5):
    return SimilarityPostprocessor(threshold=threshold)
