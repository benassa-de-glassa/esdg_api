import os
import sys
import itertools

from flask import render_template, request, jsonify

import pandas as pd
import numpy as np

from . import main_view

from util import listbox, dataframe

## DEFINITIONS
CWD = os.getcwd()
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data') # r'E:/SSD/DATA'# os.path.join(CWD, 'data') 

@main_view.route('/')
@main_view.route('/index')
def index():
    return render_template('index.html', title="ESDG")

@main_view.route('/ajax/index/folder_listbox', methods=['GET'])
def folder_option():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which host the databases
    """
    return listbox.list_to_option(os.listdir(DATA_WORKING_DIRECTORY))


@main_view.route('/ajax/index/dataset_listbox', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    folder = request.args.get('selected_folder')
    return listbox.list_to_option(os.listdir(os.path.join(DATA_WORKING_DIRECTORY, folder)))

@main_view.route('/ajax/index/country_listbox', methods=['GET'])
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
    
@main_view.route('/ajax/index/data_table', methods=['GET'])
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

@main_view.route('/ajax/index/data_table_json', methods=['GET'])
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
    
    return dataframe.select_dataframe(FILE_NAME, COUNTRIES, PRODUCTS, ELEMENTS).to_json()


