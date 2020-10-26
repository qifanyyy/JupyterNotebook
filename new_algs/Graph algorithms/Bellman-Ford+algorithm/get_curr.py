import json
import requests
import itertools
import pandas as pd
import numpy as np
import math
from graph.API_KEYS import *
from graph.config import *


def get_curr_combos(combos):

    '''
    Makes four lists each contains curriencies that
    complement its opposing list at the same index
    '''

    _to = []
    _from = []
    _to_same = []
    _from_same = []
    mix_curr = list(itertools.product(combos, combos))                          # cross all the curriences
    for d_curr in mix_curr:
        if  d_curr[0] == d_curr[1]:                                             # only join different curriences, ignore the same ones
            _from_same.append(d_curr[0])
            _to_same.append(d_curr[1])

        else:
            _from.append(d_curr[0])
            _to.append(d_curr[1])

    return _to, _from, _to_same, _from_same

def get_all_exhange_rates(_to, _from):

    '''
    Get all exhange rates for currency A to B in JSON
    '''

    all_combos = []
    for x in range(0, len(_to)):
        all_combos.append(_from[x]+_to[x])

    all_combos = ','.join(all_combos)                                       # join all currencies in list
    rates = requests.get(BASE_URL + QUOTES + all_combos + API_TOKEN1)       # get rates from API
    all_info = json.loads(rates.content)                                    # load into json format

    return all_info, all_combos


def edge_val(val):
    return (-1)*math.log(val, 2.0)


def get_df_matrix(all_info, all_combos, _to, _from, _to_same, _from_same):

        '''
        Sort all JSON and lists into a clean
        dataframe and matrix containing important
        values to be passed onto algorithm module
        '''

        df = pd.DataFrame(all_info)
        df['edge_weight'] = df['price'].apply(edge_val)
        df['to'] = _to #add extra 'to' and 'from' columns for easier accessability
        df['from'] = _from

        timestamp = df.loc[(0), ('timestamp')] #set time for this dataset

        for x in range(0, len(_to_same)):
            d = {'ask': [1], 'bid': [1], 'price': [1], \
                'symbol':[_to_same[x] + _from_same[x]], \
                'timestamp': timestamp, 'edge_weight': [0], \
                'to': [_to_same[x]], 'from': [_from_same[x]]}

            df2 = pd.DataFrame(data=d)
            df = df.append(df2, ignore_index=True)

        df = df.reset_index(drop=True)
        df = df.sort_values(by=['symbol'])
        df = df.set_index('symbol')

        matrix = df.pivot(index='from', columns='to', values='edge_weight')

        #df = pd.DataFrame.from_csv('C:/Users/Gushihahapro/Documents/Github/shortest_path/currs/test_file.csv')        # TODO THIS DATAFRAME IS FOR TESTING BASED ON THE TESTING_FILE.CSV VALUES

        return df, matrix

def get_data(currs):

    '''
    Accessable function from exterior modules
    to get dataframe and matrix, providing valid
    list of curriences as input
    '''

    _to, _from, _to_same, _from_same = get_curr_combos(currs)
    a, b = get_all_exhange_rates(_to, _from)
    df, matrix = get_df_matrix(a, b, _to, _from, _to_same, _from_same)

    table_dict = df.to_dict(orient='records')

    return df, matrix, table_dict






#print (a)
#print (b)
#
