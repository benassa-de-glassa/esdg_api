import numpy as np
import pandas as pd

def get_data_frame(FILE_NAME):
    """
    wrapper to get pandas DATAFRAME for any available data format
    """
    if FILE_NAME.endswith('.csv'):
        DATA = pd.read_csv(FILE_NAME)
    elif FILE_NAME.endswith('.sas7bdat'):
        DATA = pd.read_sas(FILE_NAME, encoding='iso-8859-1')
    return DATA

def get_dimension_names(FILE_NAME):
    if FILE_NAME.endswith('.csv'):
        DATA = pd.read_csv(FILE_NAME)
    elif FILE_NAME.endswith('.sas7bdat'):
        DATA = pd.read_sas(FILE_NAME, encoding='iso-8859-1')
    DATA.columns = map(str.lower, DATA.columns)
    country_list = np.unique(DATA['countries']) 
    product_list = np.unique(DATA['products'])
    element_list = np.unique(DATA['elements'])
    
    print('header: ', DATA.columns, '\n')
    return country_list, product_list, element_list

def select_dataframe(FILE_NAME, COUNTRIES, PRODUCTS, ELEMENTS):
    ''' select the rows according to the elements in COUNTIRES, PRODUCTS, ELEMENTS'''
    
    if FILE_NAME.endswith('.csv'):
        DATA = pd.read_csv(FILE_NAME)
    elif FILE_NAME.endswith('.sas7bdat'):
        DATA = pd.read_sas(FILE_NAME, encoding='iso-8859-1')
    else: 
        raise AssertionError(' file cannot be read, you fucked up\n')
    
    DATA.columns = map(str.lower, DATA.columns)
    print(DATA)
    print(list(DATA))

    country_rows = DATA['countries'].isin( COUNTRIES).values
    product_rows = DATA['products'].isin( PRODUCTS).values
    element_rows = DATA['elements'].isin( ELEMENTS).values

    rows = np.argwhere(country_rows * product_rows * element_rows).flatten()

    return DATA.iloc[rows, :]
