from src.utils.findPath import find_relative_path as fp
from src.rag.utils.renamer import rename_file
from src.utils.logger import setup_logger
from llama_index.core import Document
from typing import List
# import scipdf
import json
# import pickle

logger = setup_logger(__name__)


def scipdf_parser(pdf_path: str, dir_path: str, alias: int) -> List[Document]:

    article_dict = scipdf.parse_pdf_to_dict(pdf_path, parse_figures=False, 
                                            #grobid_url="https://kermitt2-grobid.hf.space"
                                            )
    if article_dict is None:
        logger.info(f'Failed to parse article {pdf_path} -- returned None []')
        return []
    
    logger.info(f"Parsed article {article_dict['title']} with alias {alias} from {pdf_path}")
    
    pdf_path = rename_file(original_path=pdf_path, article_dict=article_dict)
    logger.info(f"File renamed to {pdf_path}")

    scipdf.parse_figures(pdf_path, output_folder=f"{fp(target='algo-rag')}/outputs/{pdf_path.split('/')[-1].split('.')[0]}")  # folder should contain only PDF files
    logger.info(f"Figures parsed from {pdf_path}")

    # Create a Document objects
    abstract = Document(
        text=article_dict['abstract'], 
        metadata = {
            'paper_title': article_dict['title'],
            'section_heading': 'Abstract', 
            'authors': article_dict['authors'],
            'pub_date': article_dict['pub_date'],
            'doi': article_dict['doi'],
            'source_path': dir_path,
            'alias': alias,
        }
    )
    

    # define list of documents for the sections
    paper_documents = [abstract]
    for parsed_section in article_dict['sections']:

        for figure_id in parsed_section['figure_ref']:
            for figure in article_dict['figures']:
                if figure['figure_id'] == figure_id:
                    # Check if 'figure_type_label' is in figure
                    if 'figure_type_label' in figure:
                        figure_type_label = figure['figure_type_label']
                    else:
                        figure_type_label = 'unknown'
                        # This is a good place to add your debugging code
                        print(f"figure_type_label missing for figure_id: {figure_id}")
            
        section = Document(
            text = parsed_section['text'], 
            metadata = {
                'paper_title': article_dict['title'],
                'section_heading': parsed_section['heading'],
                'authors': article_dict['authors'],
                'pub_date': article_dict['pub_date'],
                'doi': article_dict['doi'],
                'publication_ref': ','.join(parsed_section['publication_ref']),
                # 'figure_refs': ','.join(list(set([f"{pdf_path.split('/')[-1].split('.')[0]}-{figure['figure_type_label']}-1.png" for figure_id in parsed_section['figure_ref'] for figure in article_dict['figures'] if figure['figure_id'] == figure_id]))),
                'figure_refs': ','.join(list(set([f"{pdf_path.split('/')[-1].split('.')[0]}-{figure['figure_type_label'] if 'figure_type_label' in figure else 'unknown'}-1.png" for figure_id in parsed_section['figure_ref'] for figure in article_dict['figures'] if figure['figure_id'] == figure_id]))),
                'table_refs': ','.join(list(set([f"{pdf_path.split('/')[-1].split('.')[0]}-{figure['figure_type_label'] if 'figure_type_label' in figure else 'unknown'}-1.png" for figure_id in parsed_section['table_ref'] for figure in article_dict['figures'] if figure['figure_id'] == figure_id]))),
                'source_path': dir_path,
                'alias': alias,
            }
        )
        paper_documents.append(section)
    
    return paper_documents
