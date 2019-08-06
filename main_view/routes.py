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
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data')

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
    return listbox.list_to_option(os.listdir('data'))


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
    
    country_list = np.unique(pd.read_csv(FILE_NAME)['countries'])
    product_list = np.unique(pd.read_csv(FILE_NAME)['products'])
    element_list = np.unique(pd.read_csv(FILE_NAME)['elements'])

    return {
     'countries':listbox.list_to_option(country_list),
     'products':listbox.list_to_option(product_list),
     'elements':listbox.list_to_option(element_list),
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


@main_view.route('/barplot')
def barplot():
    return render_template('bar_plot.html', title="ESDG - Barplot")

