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
    group = request.args.get('groups')

    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        datasets = [{'value': index, 'label': value.replace(',', ''), 'type': 'dataset'}
                    for index, value in enumerate(f[group].keys())]
        return jsonify(dataset=datasets)


@api.route('/api/meta', methods=['GET'])
def country_option():
    """
    return jsonify response of metadata
    """
    group = request.args.get('groups')
    dataset = request.args.get('dataset')

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

    # get the dimension names
    meta = [*request.args][2:]

    # get the file
    group = request.args.get('groups')
    dataset = request.args.get('dataset')

    # open the hdf5 file
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        # shortcut for data
        data_table = f["{}/{}".format(group, dataset)]
        data_table_shape = data_table.shape

        # shortcut for headers
        header = data_table.attrs['headers']

        # array of row numbers which are available in the data frame
        available_lines = np.arange(data_table_shape[0])

        # initialization of the selected set variables
        lines = np.arange(data_table_shape[0])

        zero_is_valid_line = True
        # iterate over all dimensions specified in the request
        inverted_conversion_dicts = []
        for dimension in meta:
            # grab all values of the dimesion
            requested_values = request.values.getlist('{}'.format(dimension))[0].split(',')
            # table containing the conversion from name to 
            conversion_table = data_table.attrs['{}_attribution'.format(dimension)]
            conversion_dict = {item[1]: item[0] for item in conversion_table}
            inverted_conversion_dicts.append({value: item for item, value in conversion_dict.items()})


            # convert the requsted values to the corresponding dimension item code
            requested_codes = [float(conversion_dict[value]) for value in requested_values]
            print(requested_values)
            print(type(requested_codes[0]))

            # get the column in which the codes are used
            column_index = np.where(conversion_table[0][0] == header)[0]

            # find the lines which match the codes
            mask = np.in1d(data_table[:, column_index], requested_codes)
            print(dimension, np.sum(mask))
            # update the lines set
            lines *= mask
            print(set(available_lines * mask))

            # the line 0 has to be checked additionally as every 'False' mask index adds the 0 index to the set
            zero_is_valid_line *= mask[0] == True

        # sort the lines
        lines = sorted(list(set(lines)))
        if not zero_is_valid_line: lines.remove(0)

        # initialize the data list
        data = []
        for line in lines:
            # add the dict formated line to data which will then be returned
            data.append({header[i]: np.nan_to_num(data_table[line, i]) for i in range(len(header)-len(meta))})
            data[-1].update({
                header[i]: inverted_conversion_dicts[j][data_table[line, i]] for j, i in enumerate(range(len(header)-len(meta), len(header)))
                })
        header_dict = [{'name': item, 'type': 'string'} for item in header]
        columns = [{'text': item, 'datafield': item, 'width': '100px'} for item in header]

        return jsonify(header=header_dict, columns=columns, data = data)
