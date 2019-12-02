import os
import sys
import itertools

from flask import render_template, request, jsonify

import numpy as np
import h5py

from . import api


## DEFINITIONS
CWD = os.getcwd()
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data/database.hdf5') # r'E:/SSD/DATA'# os.path.join(CWD, 'data') 

@api.route('/api/groups', methods=['GET'])
def folder_option():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which host the databases
    """
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        return jsonify(groups = list(f.keys()))


@api.route('/api/dataset', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    dataset = request.args.get('dataset')
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        return jsonify(groups = list(f[dataset].keys()))

@api.route('/api/meta', methods=['GET'])
def country_option():
    """
    return the list of available countries from the csv file to which the first two listboxes point
    """
    FOLDER = request.args.get('selected_folder')
    DATASET = request.args.get('selected_dataset')
    
    FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, FOLDER, DATASET)
    
    country, product, element = dataframe.get_dimension_names(FILE_NAME)

    
    return {
     'countries':listbox.list_to_option(country),
     'products':listbox.list_to_option(product),
     'elements':listbox.list_to_option(element),
    }
    
@api.route('/api/data', methods=['GET'])
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
    
    return dataframe.select_dataframe(FILE_NAME, COUNTRIES, PRODUCTS, ELEMENTS).to_html()