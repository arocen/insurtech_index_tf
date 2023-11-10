# test preprocess

import preprocess as pr
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

doc_folder_path = os.environ.get('doc_folder_path')
cut_sentences_by_year_folder = os.environ.get('cut_sentences_by_year_folder')
cut_paragraphs_by_year_folder = os.environ.get('cut_paragraphs_by_year_folder')

def testSentences():
    docs_by_year = pr.load_doc()
    cleaned_docs_by_year = pr.remove_nonsense(docs_by_year)
    new_cleaned_docs_by_year = pr.remove_href(cleaned_docs_by_year)
    splitted_docs = pr.split_docs(new_cleaned_docs_by_year)
    sentences = pr.split_into_sentences(splitted_docs)

    # cut into words
    cut_sentences = pr.cut(sentences)
    print(len(cut_sentences))

    # save cut sentences as external txt file
    pr.save_sentences(cut_sentences)
    return
    
def testParagraphs():
    docs_by_year = pr.load_doc()
    cleaned_docs_by_year = pr.remove_nonsense(docs_by_year)
    new_cleaned_docs_by_year = pr.remove_href(cleaned_docs_by_year)
    splitted_docs = pr.split_docs(new_cleaned_docs_by_year)

    # split each doc into paragraphs
    paragraphs = pr.split_into_paragraphs(splitted_docs)

    # cut into words
    cut_paragraphs = pr.cut(paragraphs)
    print(len(cut_paragraphs))

    # save cut paragraphs as external txt file
    pr.save_sentences(cut_paragraphs, cut_sentences_path=os.environ.get("cut_paragraphs_path"))
    return


def testSentencesByYear():
    docs_by_year = pr.load_doc()
    filenames = sorted([f for f in os.listdir(doc_folder_path) if f.endswith(".txt")])
    years = [filename[:4] for filename in filenames]
    save_names = [year + "_cut.txt" for year in years]
    save_paths = [os.path.join(cut_sentences_by_year_folder, save_name) for save_name in save_names]
    
    cleaned_docs_by_year = pr.remove_nonsense(docs_by_year)
    new_cleaned_docs_by_year = pr.remove_href(cleaned_docs_by_year)

    # list of lists
    splittedDocsByYear = pr.split_docs_by_year(new_cleaned_docs_by_year)
    cutSentencesByYear = []
    
    for docs, save_path in zip(splittedDocsByYear, save_paths):
        sentences = pr.split_into_sentences(docs)
        cut_sentences = pr.cut(sentences)
        cutSentencesByYear.append(cut_sentences)

        # save by year        
        pr.save_sentences(cut_sentences, save_path)

def testParagraphsByYear():
    docs_by_year = pr.load_doc()
    filenames = sorted([f for f in os.listdir(doc_folder_path) if f.endswith(".txt")])
    years = [filename[:4] for filename in filenames]
    save_names = [year + "_cut.txt" for year in years]
    save_paths = [os.path.join(cut_paragraphs_by_year_folder, save_name) for save_name in save_names]
    
    cleaned_docs_by_year = pr.remove_nonsense(docs_by_year)
    new_cleaned_docs_by_year = pr.remove_href(cleaned_docs_by_year)

    # list of lists
    splittedDocsByYear = pr.split_docs_by_year(new_cleaned_docs_by_year)
    cutParagraphsByYear = []
    
    for docs, save_path in zip(splittedDocsByYear, save_paths):
        paras = pr.split_into_paragraphs(docs)
        cut_paras = pr.cut(paras)
        cutParagraphsByYear.append(cut_paras)

        # save by year        
        pr.save_sentences(cut_paras, save_path)

# testParagraphs()
# testSentences()
# testSentencesByYear()
testParagraphsByYear()