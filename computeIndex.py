# compute index per year per company based on matrix
import pandas as pd

def sumTfPerCompany(matrix:pd.DataFrame)->pd.DataFrame:
    '''sum term frequencies per company'''
    matrix.loc['total'] = matrix.sum(numeric_only=True, axis=0)
    return matrix.loc['total']