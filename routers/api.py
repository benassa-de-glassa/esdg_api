import h5py
import numpy as np
import os
from fastapi import APIRouter
from starlette.requests import Request

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
        # years = attributes ['years'].tolist()
        for item in attributes['dimensions']:
            meta[item] = [{ _item[1]: _item[0]}
                          for _item in attributes['{}'.format(item)][1:]]

        return {
            'attributes': attributes['dimensions'].tolist(),
            'meta': meta
        }


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
            requested_codes = request.query_params['{}'.format(dimension)].split(',')
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
        rows = sorted(list(set(available_rows)))
        if not zero_is_valid_row:
            rows.remove(0)

        data = {}
        for row in rows:
            # add the dict formated line to data which will then be returned
            data[int(row)] = data_table[row, columns].tolist()

        header = tuple (header[columns].tolist())

        return {
            'header': header,
            'data': data
        }
