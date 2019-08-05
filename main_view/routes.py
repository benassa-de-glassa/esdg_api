import os
import sys
import itertools

from flask import render_template, request, jsonify

import pandas as pd
import numpy as np
from main_view import app

from util import listbox

## DEFINITIONS
CWD = os.getcwd()
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="TESt")

@app.route('/ajax/folder_listbox', methods=['GET'])
def folder_option():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which host the databases
    """
    CWD = os.getcwd()
    folders = []
    html = ''
    for i, element in enumerate(os.listdir('data')):
        folder_path = os.path.join(CWD, element)
        folders.append(element)

    return listbox.list_to_option(os.listdir('data'))


@app.route('/ajax/dataset_listbox', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    file_list = []
    folder = request.args.get('selected_folder')
    for dataset in os.listdir(os.path.join(DATA_WORKING_DIRECTORY, folder)):
        file_list.append(dataset)
    return listbox.list_to_option(file_list)

@app.route('/ajax/country_listbox', methods=['GET'])
def country_option():
    """
    return the list of available countries from the csv file to which the first two listboxes point
    """
    FOLDER = request.args.get('selected_folder')
    DATASET = request.args.get('selected_dataset')
    
    FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, FOLDER, DATASET)
    
    country_list = np.unique(pd.read_csv(FILE_NAME)['countries'])
    product_list = np.unique(pd.read_csv(FILE_NAME)['products'])
    element_list = np.unique(pd.read_csv(FILE_NAME)['elements'])

    return {
     'countries':listbox.list_to_option(country_list),
     'products':listbox.list_to_option(product_list),
     'elements':listbox.list_to_option(element_list),
    }
    
@app.route('/ajax/data_table', methods=['GET'])
def data_set_table():
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
    
    
    DATA = pd.read_csv(FILE_NAME)

    country_rows = DATA['countries'].isin( COUNTRIES).values
    product_rows = DATA['products'].isin( PRODUCTS).values
    element_rows = DATA['elements'].isin( ELEMENTS).values

    rows = np.argwhere(country_rows * product_rows * element_rows).flatten()

    RETURN_DF = DATA.iloc[rows, :]
    return RETURN_DF.to_html()



