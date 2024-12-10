import computeIndex as ci
import pandas as pd
import getMatrix as gm
import preprocess as pr
import os
from dotenv import load_dotenv

keywords_path = os.environ.get("keywords_path")
keywords_path2 = os.environ.get("keywords_path2")
company_names_path = os.environ.get("company_names_path")
matrix_save_path = os.environ.get("matrix_save_path")
cut_sentences_path = os.environ.get("cut_sentences_path")
names_excel = os.environ.get("comnpany_names_excel")
test_doc_folder_path = os.environ.get(os.environ.get("test_doc_folder_path"))
test_save_index=os.environ.get(os.environ.get("test_save_index"))

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

def testGetIndex():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    matrix = gm.init_matrix(keywords, company_names)
    corpus_list = pr.load_preprocessed_multi_corpus()
    matrices = gm.get_multi_matrices(keywords, company_names, matrix, corpus_list)
    
    # show count result
    # for m in matrices:
    #     print(m)

    years = pr.getYearFromFilename()
    indexByYear = ci.getIndex(matrices, years, company_names)
    print(indexByYear)
    return indexByYear

def testDivide():
    keywords = gm.load_words(keywords_path)
    company_names = gm.load_words(company_names_path)
    matrix = gm.init_matrix(keywords, company_names)
    corpus_list = pr.load_preprocessed_multi_corpus()
    matrices = gm.get_multi_matrices(keywords, company_names, matrix, corpus_list)
    years = pr.getYearFromFilename()
    indexByYear = ci.getIndex(matrices, years, company_names)

    # drop columns contain zeros only
    indexByYear = ci.dropZeros(indexByYear)
    print(indexByYear)

    countWords = ci.countWords(corpus_list, years)
    print(countWords)
    weights = ci.weightFromCountWords(countWords)
    print(weights)
    newIndices = ci.divideByWordNum(indexByYear, weights)
    print(newIndices)
    return newIndices

def testLoadExcel():
    keywords = gm.load_words(keywords_path)
    names = gm.load_excel(names_excel)
    # print(names)
    index_names = gm.getIndexNames(names)
    matrix = gm.init_matrix(keywords, index_names)
    corpus_list = pr.load_preprocessed_multi_corpus(folder_path=os.environ.get("cut_paragraphs_by_year_folder")) # use cut paragraphs corpus
    matrices = gm.count_multi_names_by_year(keywords, names, matrix, corpus_list)
    years = pr.getYearFromFilename()
    indexByYear = ci.getIndex(matrices, years, index_names)

    # drop columns contain zeros only
    indexByYear = ci.dropZeros(indexByYear)
    # print(indexByYear)

    countWords = ci.countWords(corpus_list, years)
    # print(countWords)
    weights = ci.weightFromCountWords(countWords)
    # print(weights)
    newIndices = ci.divideByWordNum(indexByYear, weights)
    print(newIndices)
    newIndices.to_excel(os.environ.get("save_indices"))
    return newIndices

def testLoadExcelNOtWeighted():
    keywords = gm.load_words(keywords_path)
    names = gm.load_excel(names_excel)
    # print(names)
    index_names = gm.getIndexNames(names)
    matrix = gm.init_matrix(keywords, index_names)

    # choose 1 of 2 below
    # corpus_list = pr.load_preprocessed_multi_corpus(folder_path=os.environ.get("cut_paragraphs_by_year_folder")) # use cut paragraphs corpus
    corpus_list = pr.load_preprocessed_multi_corpus(folder_path=os.environ.get("cut_sentences_by_year_folder")) # use cut sentences corpus

    matrices = gm.count_multi_names_by_year(keywords, names, matrix, corpus_list)

    years = pr.getYearFromFilename()
    indexByYear = ci.getIndex(matrices, years, index_names)

    # drop columns contain zeros only
    indexByYear = ci.dropZeros(indexByYear)
    # print(indexByYear)
    print(indexByYear)
    indexByYear.to_excel(os.environ.get("save_indices"))
    return indexByYear

def testExtraKeywords():
    keywords = gm.load_words(keywords_path)
    keywords2 = gm.load_words(keywords_path2)
    keywords = list(set(keywords + keywords2))
    # num_words = len(keywords)
    # print(num_words)

    names = gm.load_excel(names_excel)
    # print(names)
    index_names = gm.getIndexNames(names)
    matrix = gm.init_matrix(keywords, index_names)
    corpus_list = pr.load_preprocessed_multi_corpus(folder_path=os.environ.get("cut_sentences_by_year_folder")) # use cut sentences corpus
    # corpus_list = pr.load_preprocessed_multi_corpus(test_doc_folder_path)    # use 1 year corpus to test
    matrices = gm.count_multi_names_by_year(keywords, names, matrix, corpus_list)

    print(len(matrices))
    years = pr.getYearFromFilename()

    # save per year data
    # writer = pd.ExcelWriter(os.environ.get("test_save_index"), engine='xlsxwriter')
    # for df, year in zip(matrices, years):
    #     df.to_excel(writer, sheet_name=year)


    indexByYear = ci.getIndex(matrices, years, index_names)

    # drop columns contain zeros only
    # indexByYear = ci.dropZeros(indexByYear)

    print(indexByYear)
    indexByYear.to_excel(os.environ.get("save_indices"))
    # indexByYear.to_excel(os.environ.get("test_save_index")) # save test result
    return indexByYear



# testSum()
# testGetIndex()
# testDivide()
testExtraKeywords()