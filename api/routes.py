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
        groups = [{'value': index, 'label': value.replace(',', ''), 'type': 'groups'} \
            for index, value in enumerate(f.keys())]
        return jsonify(groups=groups)


@api.route('/api/dataset', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    dataset = request.args.get('dataset')

    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        datasets = [{'value': index, 'label': value.replace(',', ''), 'type': 'dataset'}
                    for index, value in enumerate(f[dataset].keys())]
        return jsonify(dataset=datasets)


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
            meta[item] = [{'value': _item[0], 'label': _item[1].replace(',', ''), 'type': item} \
                for _item in attributes['{}_attribution'.format(item)][1:]]

        return jsonify(attributes=attributes['attributions'].tolist(), meta=meta)


@api.route('/api/data', methods=['GET'])
def data_set_table():
    """
    return the files in the folder selected as 
    """

    meta = [*request.args][2:]
    # print(meta)
    # get the file
    group = request.args.get('groups')
    dataset = request.args.get('dataset')

    # FILE_NAME = os.path.join(DATA_WORKING_DIRECTORY, group, dataset)

    # # get the selected rows
    # COUNTRIES = request.values.getlist('selected_countries[]')
    # PRODUCTS = request.values.getlist('selected_products[]')
    # ELEMENTS = request.values.getlist('selected_elements[]')

    # TODO:
    # - find and identify the meta-tags with the corresponding codes
    # - find the correct rows to add to 'data'-variable
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        data_table = f["{}/{}".format(group, dataset)]
        data_table_shape = data_table.shape

        header = data_table.attrs['headers']

        available_lines = np.arange(data_table_shape[0])

        lines = set()

        for dimension in meta:
            # get the name of the selected dimension tags from the request

            requested_values = request.values.getlist('{}'.format(dimension))[0].split(',')
            print(requested_values)
            # table containing the conversion from name to 
            conversion_table = data_table.attrs['{}_attribution'.format(dimension)]
            conversion_dict = {item[1]: item[0] for item in conversion_table}

            # get the column in which the codes are used
            column_index = np.where(conversion_table[0][0] == header)[0]

            # convert the requsted values to the corresponding dimension item code
            requested_codes = [float(conversion_dict[value]) for value in requested_values]

            # iterate through all lines
            # print(np.sum( np.array([bool(x in requested_codes) for x in data_table[:, column_index]])))


            # print(data_table[:, column_index], requested_codes)
            mask = np.in1d(data_table[:, column_index], requested_codes)
            lines.update(set(mask * available_lines))
            if not mask[0]: lines.discard(0)


        lines = sorted(list(lines))
        # lines *= np.array([bool(x in requested_codes) for x in data_table[:, column_index]])

        
        data = []
        for line in lines:
            data.append({header[i]: np.nan_to_num(data_table[line, i]) for i in range(len(header)-len(meta))})
        return jsonify( data = data)
