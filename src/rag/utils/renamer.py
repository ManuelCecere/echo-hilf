from src.utils.logger import setup_logger
from llama_index.llms.openai import OpenAI
from typing import List, Optional
import os
import re

# set up logging
logger = setup_logger(__name__)

def is_valid_filename(filename: str, placebo: bool = False) -> bool:

    if placebo:
        return False

    pattern = r'^[a-zA-Z0-9_]+\.pdf$'
    return bool(re.match(pattern, filename))


def extract_keywords(text: str, num_keywords: int = 7) -> List[str]:
    
    llm = OpenAI(model='gpt-3.5-turbo-0125', temperature=0.0, api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"Summarize in {num_keywords} words the text below here. "\
               "You should summarize the text as concisely as possible so that a person can understand the topic just by reading those words. "\
              f"\n\n{text} \n\n"\
               "Summarization:"
    keywords = llm.complete(prompt).text

    return keywords

def get_new_name_file(original_filename: str, article_dict: dict,  cut_length: Optional[int] = 80) -> str:

    proper_title = isinstance(article_dict['title'], str) and 10 <= len(article_dict['title']) <= 200
    proper_abstract = isinstance(article_dict['abstract'], str) and len(article_dict['abstract']) > 50
    proper_first_section = isinstance(article_dict['sections'][0]['text'], str) and len(article_dict['sections'][0]['text']) > 50
    
    if proper_title:
        prefix = article_dict['title']
    elif not proper_title and proper_abstract:
        prefix = extract_keywords(article_dict['abstract'])
    elif not proper_title and not proper_abstract and proper_first_section:
        prefix = extract_keywords(article_dict['sections'][0]['text'])

    else: 
        logger.error("No valid title, abstract, or first section found in the article_dict")
        raise ValueError("No valid title, abstract, or first section found in the article_dict")

    prefix = re.sub(r'[^a-zA-Z0-9_]+', '_', prefix).strip('_')
    prefix = prefix[:cut_length] if len(prefix) > cut_length else prefix
    new_filename = f"{prefix.lower()}{os.path.splitext(original_filename)[1]}"

    return new_filename

def rename_file(original_path: str, article_dict: dict) -> str:

    # get the filename from the path, which is the last part of the path
    original_filename = os.path.basename(original_path)
    directory_path = os.path.dirname(original_path)

    # check if the filename is valid
    if is_valid_filename(filename=original_filename, placebo=True):
        logger.info(f"Filename {original_filename} is valid")
        return original_path

    # get the new filename
    new_filename = get_new_name_file(original_filename=original_filename, article_dict=article_dict)
    logger.info(f"Renaming {original_filename} to {new_filename}")
    new_path = os.path.join(directory_path, new_filename)

    # rename the file
    os.rename(original_path, new_path)
    
    return new_path
    
if __name__ == "__main__":
    abstract = "We present a new major release of the OpenSubtitles collection of parallel corpora. \
The release is compiled from a large database of movie and TV subtitles and includes a total of 1689 bitexts \
spanning 2.6 billion sentences across 60 languages. The release also incorporates a number of enhancements \
in the preprocessing and alignment of the subtitles, such as the automatic correction of OCR errors \
and the use of meta-data to estimate the quality of each subtitle and score subtitle pairs."
    #keywords = extract_keywords(abstract)
    #print(keywords)
    b = is_valid_filename('prova.pdf')
    b = is_valid_filename("p rova.pdf")
    b = is_valid_filename("pr'ova.pdf")

    #print(is_valid_filename("doc_1_We_present_a_new_major_release_of_the_OpenSubtitles_collection_of_parallel_corpora.pdf"))
    #print(is_valid_filename("d_We_present_a_new_major_release_of_the_OpenSubtitles_collection_of_parallel_corpora.pdf"))