import os
import sys
import itertools

from flask import render_template, request, jsonify

import numpy as np
import h5py

from . import api


## DEFINITIONS
CWD = os.getcwd()
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data/database.hdf5')


@api.route('/api/groups', methods=['GET'])
def folder_option():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which host the databases
    """
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        groups = [{'value': index, 'label': value} \
            for index, value in enumerate(f.keys())]
        return jsonify(groups=groups)


@api.route('/api/dataset', methods=['GET'])
def data_set_option():
    """
    return the files in the folder selected as 
    """
    group = request.args.get('groups')

    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        datasets = [{'value': index, 'label': value, 'type': 'dataset'}
                    for index, value in enumerate(f[group].keys())]
        return jsonify(dataset=datasets)


@api.route('/api/meta', methods=['GET'])
def meta_option():
    """
    return jsonify response of metadata
    """
    group = request.args.get('groups')
    dataset = request.args.get('dataset')

    meta = {}
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["{}/{}".format(group, dataset)].attrs
        # years = attributes ['years'].tolist()
        for item in attributes['dimensions']:
            meta[item] = [{'value': _item[1], 'label': _item[0]} \
                for _item in attributes['{}'.format(item)][1:]]

        return jsonify(attributes=attributes['dimensions'].tolist(), meta=meta)


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
        # get the data table
        data_table = f["{}/{}".format(group, dataset)]

        # grab the header attribute
        header = data_table.attrs['headers']
        available_rows = np.arange(data_table.shape[0], dtype = int)

        zero_is_valid_row = True

        for dimension in meta:
            requested_codes = request.values.getlist('{}'.format(dimension))[0].split(',')
            requested_codes = np.asarray(requested_codes, dtype = int)

            conversion_dict = {int(entry[1]): entry[0] for entry in data_table.attrs['{}'.format(dimension)][1:]}
            # requested_codes = np.asarray(requested_codes, dtype = np.int8)
            if dimension == 'years':
                # the requested columns always contain the requested dimensions
                columns = list(range(len(meta)-1))
                # add columns for each requested year
                for year in requested_codes:
                    # convert each year to the corresponding label
                    columns.append(np.where(conversion_dict[year] == header)[0][0])
            else:
                # get the column in which the codes are used
                column_index = np.where(data_table.attrs['{}'.format(dimension)] [0][1] == header)[0]

                # find the lines which match the codes
                mask = np.in1d(data_table[:, column_index], requested_codes)
                available_rows *= mask

                # the line 0 has to be checked additionally as every 'False' mask index adds the 0 index to the set
                zero_is_valid_row *= mask[0] == True
        
        # sort the lines
        rows = sorted(list(set(available_rows)))
        if not zero_is_valid_row: rows.remove(0)


        data = []
        for row in rows:
            # add the dict formated line to data which will then be returned
            data += [{int(row): data_table[row, columns].tolist()}]
            # data.append({header[i]: np.nan_to_num(data_table[line, i]) for i in range(len(header)-len(meta))})
            # data[-1].update({
            #     header[i]: inverted_conversion_dicts[j][data_table[row, i]] for j, i in enumerate(range(len(header)-len(meta), len(header)))
            #     })


        columns = list(map(str, columns))
        # return jsonify(columns)
        return jsonify(header=header.tolist(), columns=columns, data = data)
