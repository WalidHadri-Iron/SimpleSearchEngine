from app.controlname import *
import os, json
import pandas as pd
import sqlite3


with open('config.json') as json_file:
    config = json.load(json_file)

split_columns = config["split_columns"]
exclude = config["exclude"]
path_database = config["path_database"]


def return_response_sentence(input_sentence):
    response_result = return_response(path_database, input_sentence, split_columns, exclude)
    result = [ { 'index': key, 'control_name': response_result[key]['Control name'] } for key in response_result.keys() ]
    return result

def return_details(index):

    conn = sqlite3.connect(path_database)
    cur = conn.cursor()
    cur.execute('SELECT * FROM Control_table')
    dataframe = []
    for row in cur:
        dataframe.append(row)
    columns = [description[0] for description in cur.description]

    df = pd.DataFrame(dataframe)
    df.columns = columns    

    result = dict(df.iloc[index].fillna(""))
    return result
