import os
import sys
import itertools

from flask import render_template, request, jsonify

import pandas as pd
import numpy as np

from . import timeseries

from util import listbox, dataframe

## DEFINITIONS
CWD = os.getcwd()
DATA_WORKING_DIRECTORY = os.path.join(CWD, 'data')

@timeseries.route('/timeseries')
def barplot():
    return render_template('time_series.html', title="ESDG - Time Series")

# @main_view.route('/ajax/index/folder_listbox', methods=['GET'])
# def folder_option():
#     """
#     return the options for the first listbox in the main view as html options
#     i.e. the list of folders which host the databases
#     """
#     return listbox.list_to_option(os.listdir('data'))


