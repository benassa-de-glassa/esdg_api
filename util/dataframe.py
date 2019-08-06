import numpy as np
import pandas as pd

def select_dataframe(file_path, COUNTRIES, PRODUCTS, ELEMENTS):
    ''' select the rows according to the elements in COUNTIRES, PRODUCTS, ELEMENTS'''
    DATA = pd.read_csv(file_path)

    country_rows = DATA['countries'].isin( COUNTRIES).values
    product_rows = DATA['products'].isin( PRODUCTS).values
    element_rows = DATA['elements'].isin( ELEMENTS).values

    rows = np.argwhere(country_rows * product_rows * element_rows).flatten()

    return DATA.iloc[rows, :]