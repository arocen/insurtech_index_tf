# get co-occurrence matrix of collected words and company names from cut sentences after preprocessing

import pandas as pd


def load_words(path:str)->list:
    '''
    读取对应路径的关键词或者公司名, 返回列表, 每一行的词为列表的一个元素.
    used to load keywords and company names
    '''
    words = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            cleaned_line = line.strip()
            words.append(cleaned_line)
    return words

def load_excel(path:str)->list[list[str]]:
    '''
    读取公司名Excel文件
    返回列表，每个元素为一个列表，包括同一公司的不同简称
    '''
    df = pd.read_excel(path, sheet_name="财险公司", usecols="B")
    names = df.values.tolist()
    names = [name[0].split(" ") for name in names]
    return names

def getIndexNames(names:list[list[str]])->list:
    '''返回用于初始化矩阵的唯一公司名'''
    return [company[0] for company in names]


def init_matrix(keywords:list[str], company_names:list[str])->pd.DataFrame:
    '''initialize 0 values matrix from collected words and company names'''
    matrix = pd.DataFrame(0, index=keywords, columns=company_names)
    return matrix


def count_co_occur(keywords:list[str], company_names:list[str], matrix:pd.DataFrame, corpus:list[str])->pd.DataFrame:
    '''
    iterate every sentence and count co-occurrence
    count co-occurrence in each element of corpus
    company_names are column labels of matrix, keywords are row labels
    '''
    for text in corpus:
        wlist = text.split(" ")
        for name in company_names:
            if name in wlist:
                for keyword in keywords:
                    if keyword in wlist:
                        count = wlist.count(keyword)
                        matrix.at[keyword, name] += count
                    else:
                        continue
            else:
                continue
    
    return matrix


def count_multi_names(keywords:list[str], names:list[list[str]], matrix:pd.DataFrame, corpus:list[str])->pd.DataFrame:
    for text in corpus:
        wlist = text.split(" ")
        for company in names:
            index_name = company[0]
            for name in company:
                if name in wlist:
                    for keyword in keywords:
                        if keyword in wlist:
                            count = wlist.count(keyword)
                            matrix.at[keyword, index_name] += count
                        else:
                            continue
                else:
                    continue
    
    return matrix

def count_multi_names_by_year(keywords:list[str], names:list[list[str]], matrix:pd.DataFrame,  corpus_list:list[list[str]])->list[pd.DataFrame]:
    matrices = []
    index_names = getIndexNames(names)
    for corpus in corpus_list:
        count_result = count_multi_names(keywords, names, matrix, corpus)
        matrices.append(count_result.copy())    # use .copy() to avoid mutablity of count_result within loop
        matrix = init_matrix(keywords, index_names) # reset count of matrix to zero
    return matrices

def save_matrix(matrix:pd.DataFrame, save_path:str):
    '''save matrix to Excel'''
    matrix.to_excel(save_path)
    return


def get_multi_matrices(keywords:list[str], company_names:list[str], matrix:pd.DataFrame, corpus_list:list[list[str]])->list[pd.DataFrame]:
    
    matrices = []
    for corpus in corpus_list:
        count_result = count_co_occur(keywords, company_names, matrix, corpus)
        matrices.append(count_result.copy())    # use .copy() to avoid mutablity of count_result within loop
        matrix = init_matrix(keywords, company_names) # reset count of matrix to zero

    return matrices