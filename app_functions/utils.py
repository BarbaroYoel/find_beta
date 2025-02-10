import os
import glob
import json
import pandas as pd


def create_data_frame_establishments():
    parent_path = os.path.dirname(os.getcwd())
    files_path = os.path.join(parent_path, "data/restaurants_bars/*.json")
    json_files = glob.glob(files_path)
    data = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8-sig') as f:
            data.append(json.load(f))
    return pd.DataFrame(data)


def create_data_frame_municipality():
    parent_path = os.path.dirname(os.getcwd())
    file = os.path.join(parent_path, "data/municipality.json")
    with open(file, 'r', encoding='utf-8-sig') as f:
            data=json.load(f)
    municipality_list = [value for key, value in data.items()]
    
    return pd.DataFrame(municipality_list)


def create_data_tasteatlas():
    parent_path = os.path.dirname(os.getcwd())
    file = os.path.join(parent_path, "data/tasteatlas.json")
   
    with open(file, 'r', encoding='utf-8-sig') as f:
            data=json.load(f) 
    return data    