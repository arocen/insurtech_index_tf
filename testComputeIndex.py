import computeIndex as ci
import pandas as pd
import getMatrix as gm
import preprocess as pr
import os
from dotenv import load_dotenv

keywords_path = os.environ.get("keywords_path")
company_names_path = os.environ.get("company_names_path")
matrix_save_path = os.environ.get("matrix_save_path")
cut_sentences_path = os.environ.get("cut_sentences_path")

load_dotenv()

def testSum():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    matrix = gm.init_matrix(keywords, company_names)
    corpus = pr.load_saved_preprocessed_corpus(cut_sentences_path)
    result = gm.count_co_occur(keywords, company_names, matrix, corpus, matrix_save_path)
    sum_matrix = ci.sumTfPerCompany(result)
    print(sum_matrix)
    return

testSum()