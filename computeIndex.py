# compute index per year per company based on matrix
import pandas as pd

def sumTfPerCompany(matrix:pd.DataFrame)->pd.Series:
    '''sum term frequencies per company'''
    total = matrix.sum(numeric_only=True, axis=0) # axis=0 means sum all rows in each column
    return total


# get per year data
def getIndex(matrix_list:list[pd.DataFrame], years:list[str], company_names:list[str])->pd.DataFrame:
    '''
    return index per year per company
    '''
    results = pd.DataFrame(index=years, columns=company_names)
    for matrix, year in zip(matrix_list, years):
        index = sumTfPerCompany(matrix)
        results.loc[year] = index
    return results

def countWords(corpus_list:list[list[str]], years:list[str])->pd.Series:
    '''return total number of words per year'''
    countWords = []
    for corpus in corpus_list:
        n = 0
        for sentence in corpus:
            n += len(sentence)
        countWords.append(n)
    df = pd.Series(countWords, index=years)
    return df

def weightFromCountWords(countWords:pd.Series)->pd.Series:
    '''assign weights according to countWords'''
    total = countWords.sum() # sum all values
    # print(total)
    countWords = countWords.divide(total) # .divide does not change the original series
    return countWords

def divideByWordNum(indices:pd.DataFrame, countWords:pd.Series)->pd.DataFrame:
    '''divide indices by word number in countWords'''

    indices = indices.astype(int)
    print(indices.dtypes)
    indices = indices.div(countWords, axis=0)    # index(row labels) must be same
    
    return indices

def dropZeros(indices:pd.DataFrame)->pd.DataFrame:
    '''Drop columns that contain zeros only'''
    indices = indices.loc[:, (indices != 0).any(axis=0)]
    return indices
