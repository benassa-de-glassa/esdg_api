import os
import sys
import itertools
import json

from flask import render_template, request, jsonify

import pandas as pd
import numpy as np

from . import timeseries

from util import listbox, dataframe

from bokeh.plotting import figure
from bokeh.embed import components, json_item

## DEFINITIONS
CWD = os.getcwd()
# CWD = 'E:\\SSD\\'
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data')# r'E:/SSD/DATA'# os.path.join(CWD, 'data')

@timeseries.route('/timeseries')
def barplot():
    return render_template('time_series.html', title="ESDG - Time Series")


@timeseries.route('/ajax/timeseries/plot', methods=['GET'])
def data_set_table_json():
    """
    return the files in the folder selected as 
    """

    # get the file
    FOLDER = request.args.get('selected_folder')
    DATASET = request.args.get('selected_dataset')
    FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, FOLDER, DATASET)

    # get the selected rows
    COUNTRIES = request.values.getlist('selected_countries[]')
    PRODUCTS = request.values.getlist('selected_products[]')
    ELEMENTS = request.values.getlist('selected_elements[]')
    
    DATA_ROWS = dataframe.select_dataframe(FILE_NAME, COUNTRIES, PRODUCTS, ELEMENTS)
    print(list(DATA_ROWS))
    
    # separate the numerical from the categorical data
    # categorical_headers = ['countries', 'country_codes', 'products', 'product_codes', 'elements', 'ele_codes'] # hard coded due to different order of headers
    # numerical_headers_indices = np.zeros(len(list(DATA_ROWS)))

    # for header in categorical_headers:
    #     print('asdfadsfd', np.argwhere(list(DATA_ROWS) == header))
    #     numerical_headers += np.argwhere(header == list(DATA_ROWS))
    # print("header indices", numerical_headers_indices)
    # # for header in headers: years.remove(header)
    # # years = [int(year[1:]) for year in years]
    # print(list(DATA_ROWS))
    # # print(years)
    # print("datarows", DATA_ROWS)
    years = list(DATA_ROWS)
    if years[1] == 'country_codes': 
        years = years[6:]
        years = [int(year[1:]) for year in years]
        data = DATA_ROWS.values[:, 6:]
    elif years[1] == 'products':
        years = years[3:-3]
        years = [int(year[1:]) for year in years]
        data = DATA_ROWS.values[3: -3]
    print(years)
    p = figure()

    for row in data:
        print(row)
        p.scatter(x=years, y=row)

    script_bok, div_bok = components(p)
    
    return render_template('update_content.html', div_bok=div_bok, script_bok=script_bok)
    
