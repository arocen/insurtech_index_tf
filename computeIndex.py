# compute index per year per company based on matrix
import pandas as pd

def sumTfPerCompany(matrix:pd.DataFrame)->pd.DataFrame:
    '''sum term frequencies per company'''
    matrix.loc['total'] = matrix.sum(numeric_only=True, axis=0)
    return matrix.loc['total']


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
