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


def init_matrix(keywords:list[str], company_names:list[str])->pd.DataFrame:
    '''initialize 0 values matrix from collected words and company names'''
    matrix = pd.DataFrame(0, index=company_names, columns=keywords)
    return matrix


def count_co_occur(keywords:list[str], company_names:list[str], matrix:pd.DataFrame, corpus:list[str], save_path:str)->pd.DataFrame:
    '''
    iterate every sentence and count co-occurrence
    count co-occurrence in each element of corpus
    company_names are row labels of matrix, keywords are column labels
    '''
    for text in corpus:
        wlist = text.split(" ")
        for name in company_names:
            if name in wlist:
                for keyword in keywords:
                    if keyword in wlist:
                        count = wlist.count(keyword)
                        matrix.at[name, keyword] += count
                    else:
                        continue
            else:
                continue
    
    save_matrix(matrix, save_path)
    return matrix


def save_matrix(matrix:pd.DataFrame, save_path:str):
    '''save matrix to Excel'''
    matrix.to_excel(save_path)
    return