# test preprocess

import preprocess as pr
from dotenv import load_dotenv
import os

# load .env file
load_dotenv()

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

testParagraphs()
