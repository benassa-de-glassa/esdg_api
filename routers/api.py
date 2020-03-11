import h5py
import numpy as np
import os
from fastapi import APIRouter
from starlette.requests import Request

import pandas as pd

router = APIRouter()


## DEFINITIONS
# needs the environment variable ESDG_DATABASE_BASE to be set
DATA_WORKING_DIRECTORY = os.environ['ESDG_DATABASE_PATH']

@router.get('/groups')
def group_dict():
    """
    return the options for the first listbox in the main view as html options
    i.e. the list of folders which  the databases host
    """
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        groups = [{'value': index, 'label': value}
                  for index, value in enumerate(f.keys())]
        return {'groups': groups}


@router.get('/dataset')
def dataset_dict(groups: str):
    """
    return the files in the folder selected as
    """

    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        datasets = [{'value': index, 'label': value}
                    for index, value in enumerate(f[groups].keys())]
        return {'dataset': datasets}


@router.get('/meta')
def meta_option(groups: str, dataset: str):
    """
    return jsonify response of metadata
    """

    meta = {}
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["{}/{}".format(groups, dataset)].attrs
        print(attributes['dimensions'])
        # years = attributes ['years'].tolist()
        for item in attributes['dimensions']:
            meta[item] = {_item[1]: _item[0]
                          for _item in attributes['{}'.format(item.decode('utf-8'))][1:]}

        return {
            'attributes': attributes['dimensions'].tolist(),
            'meta': meta
        }


@router.get('/country_dimension')
def country_dimension(groups: str, dataset: str):
    """this function returns the a JSON array which includes all country-type dimensions of a given dataset

    Arguments:
        groups {str} -- name of the group/domain of the selected dataset
        dataset {str} -- name of the dataset of the selected dataset
    """
    country_dimension = []
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["{}/{}".format(groups, dataset)].attrs
        # years = attributes ['years'].tolist()
        for item in attributes['dimensions']:
            # very crude.. think of smarter way
            if item.decode('utf-8') in ['countries', 'reporter', 'partner']:
                country_dimension.append(item.decode('utf-8'))
        return country_dimension


@router.get('/country_conversion')
def country_conversion(from_code: str, to_code: str):
    """
    this function returns a JSON object from the codes used in ESDG to 
    those used in other databases which includes all country-type dimensions of 
    a given dataset

    """
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["global_conversion_tables/"].attrs["country_codes"]
        # get the column where the requested codes can be found
        from_col = np.where(attributes[0] == from_code)
        to_col = np.where(attributes[0] == to_code)

        # do not use int(float(string)) in future when database is created using db.astype(int, errors='ignore')
        return {int(float(line[from_col][0])): line[to_col][0] for line in attributes[1:]}

@router.get('/product_dimension')
def product_dimension(groups: str, dataset: str):
    """this function returns the a JSON array which includes all producy-type dimensions of a given dataset

    Arguments:
        groups {str} -- name of the group/domain of the selected dataset
        dataset {str} -- name of the dataset of the selected dataset
    """
    product_dimension = []
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        attributes = f["{}/{}".format(groups, dataset)].attrs
        # years = attributes ['years'].tolist()
        for item in attributes['dimensions']:
            # very crude.. think of smarter way
            if item.decode('utf-8') in ['products']:
                product_dimension.append(item.decode('utf-8'))
        return product_dimension

@router.get('/hs') # harmonized system
def harmonized_system(maximum_code_level: int=3):
    """
    this function returns the a JSON object from the codes used in ESDG to 
    those used in other databases which includes all country-type dimensions of 
    a given dataset

    """
    db = pd.read_excel('../db/UN Comtrade Commodity Classifications.xlsx', dtype=str, )
    db = db.replace(np.nan, '', regex=True)
    ids = db['Code'].values
    label = db['Description'].values
    parent = db['Code Parent'].values
    level = db['Level'].values

    return {product_id + 4* '0': [label[i], parent[i]+ 4* '0'] for i, product_id in enumerate(ids)}




@router.get('/data')
def data_set_table(request: Request):
    """
    return the data as specified in the request
    the request must include the desired:
        - group
        - dataset
        - at least one value for all available dimensions as returned by the meta_option function
    :param: request URLencoded request
    """

    # get the dimension names
    meta = set(request.query_params)
    meta.remove('groups')
    meta.remove('dataset')

    group = request.query_params['groups']
    dataset = request.query_params['dataset']

    # open the hdf5 file
    with h5py.File(DATA_WORKING_DIRECTORY, 'r') as f:
        # get the data table
        data_table = f["{}/{}".format(group, dataset)]

        # grab the header attribute
        header = data_table.attrs['headers']
        available_rows = np.arange(data_table.shape[0], dtype=int)

        zero_is_valid_row = True

        for dimension in meta:
            requested_codes = request.query_params['{}'.format(
                dimension)].split(',')
            requested_codes = np.asarray(requested_codes, dtype=int)

            if 'year' in dimension:

                conversion_dict = {
                    int(entry[1]): entry[0] for entry in data_table.attrs['{}'.format(dimension)][1:]}
                # the requested columns always contain the requested dimensions
                columns = list(range(len(meta)-1))
                # add columns for each requested year
                for year in requested_codes:
                    # convert each year to the corresponding label
                    columns.append(
                        np.where(conversion_dict[year] == header)[0][0])
            else:
                # get the column in which the codes are used
                column_index = np.where(
                    data_table.attrs['{}'.format(dimension)][0][1] == header)[0]

                header[column_index] = dimension
                # find the lines which match the codes
                mask = np.in1d(data_table[:, column_index], requested_codes)
                available_rows *= mask

                # the line 0 has to be checked additionally as every 'False' mask index adds the 0 index to the set
                zero_is_valid_row *= mask[0] == True

        # sort the lines
        # TODO: sorting should not be necessary?
        rows = sorted(list(set(available_rows)))
        if not zero_is_valid_row:
            rows.remove(0)

        data = {}
        for row in rows:
            # add the dict formated line to data which will then be returned
            data[int(row)] = data_table[row, columns].tolist()

        header = tuple(header[columns].tolist())

        return {
            'header': header,
            'data': data
        }
