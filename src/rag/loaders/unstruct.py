# from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import Element
from unstructured.partition.html import partition_html


# elements = partition_pdf(
#         './data/llm800/sarikaya_al_05.pdf',
#         strategy='hi_res',
#         infer_table_structure=True,
#         extract_image_block_types=["Image", "Table"],
#         extract_image_block_output_dir="./src/rag/loaders/src/rag/loaders/eg_img_down"
#         )
#
#
# for element in elements:
#     print(type(element))
#     print(element.text)
#     print('\n')

import os
from typing import List

# # Assuming partition_pdf and Element are imported from your provided context
# from unstructured.partition.pdf import partition_pdf
# from unstructured.documents.elements import Element
#
#
# def unstructured_pdf_loader(dir_path: str, pdf_path: str, alias: int) -> List[Element]:
#     # Process PDF file and return a list of elements with custom metadata
#     elements = partition_pdf(
#         filename=pdf_path,
#         strategy='hi_res',
#         infer_table_structure=True,
#         extract_image_block_types=["Image", "Table"],
#         extract_image_block_output_dir="./src/rag/loaders/src/rag/loaders/eg_img_down"
#     )
#
#     # Add custom metadata to each element
#     for element in elements:
#         if not hasattr(element, 'metadata'):
#             element.metadata = {}
#         element.metadata['source_path'] = os.path.dirname(dir_path)  # Source directory path
#         element.metadata['file_path'] = pdf_path  # Specific file path
#         element.metadata['alias'] = alias
#
#     return elements


import re

def unstructured_html_loader(dir_path: str, path: str, url: int) -> List[Element]:
    document_elements = partition_html(
        filename=path
    )
    new_els = []
    # Add custom metadata to each element
    for element in document_elements:
        if not hasattr(element, 'metadata'):
            element.metadata = {}

        new_metadata = element.metadata.to_dict()
        new_metadata['source_path'] = os.path.dirname(dir_path)  # Source directory path
        new_metadata['file_path'] = path  # Specific file path
        new_metadata['url'] = url
        element.metadata.from_dict(new_metadata)
        pattern = r'(\n+|\t+|\r+)'
        element.text = re.sub(pattern, '\n', element.text)
        element.text = re.sub(pattern, '\n', element.text)
        if element.text:
            new_els.append(element)
    return new_els
# Using partition_html to ingest HTML content
