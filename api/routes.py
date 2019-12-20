import os
import sys
import itertools

from flask import render_template, request, jsonify

import numpy as np
import h5py

from . import api


## DEFINITIONS
CWD = os.getcwd()
# DATA_WORKING_DIRECTORY = os.path.join(CWD, '/media/pi/UNTITLED/database.hdf5') 
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data/database.hdf5')

@api.route('/api/groups', methods=['GET'])
def folder_option():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which host the databases
    """
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        groups = [{'value': index, 'label': value, 'type': 'groups'} for index, value in enumerate(f.keys())]
        return jsonify(groups = groups)


@api.route('/api/dataset', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    dataset = request.args.get('dataset')

    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        datasets = [{'value': index, 'label': value, 'type': 'dataset'} for index, value in enumerate(f[dataset].keys())]
        return jsonify(dataset = datasets)

@api.route('/api/meta', methods=['GET'])
def country_option():
    """
    return jsonify response of metadata
    """
    group = request.args.get('groups')
    dataset = request.args.get('dataset')

    # FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, group, dataset)
    meta = {}
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["{}/{}".format(group, dataset)].attrs 
        # years = attributes ['years'].tolist()
        for item in attributes['attributions']:
            print(item)
            meta[item] = [{'value': _item[0], 'label': _item[1], 'type': item} \
                for _item in attributes['{}_attribution'.format(item)][1:]]
            
        return jsonify(attributes = attributes['attributions'].tolist(), meta = meta)
    
@api.route('/api/data', methods=['GET'])
def data_set_table():
    """
    return the files in the folder selected as 
    """

    # get the file
    group = request.args.get('group')
    dataset = request.args.get('dataset')
    FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, folder, dataset)

    # get the selected rows
    COUNTRIES = request.values.getlist('selected_countries[]')
    PRODUCTS = request.values.getlist('selected_products[]')
    ELEMENTS = request.values.getlist('selected_elements[]')
    
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        data_table = f["{}/{}".format(group, dataset)]
        for i in f:
            print (i)


    return jsonify("not implemented yet")