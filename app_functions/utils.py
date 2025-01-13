import os
import glob
import json
import pandas as pd

def create_data_frame():
    """
    Reads all JSON files from the 'data/restaurants_bars' directory
    and loads them into a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing all the restaurant and bar data.
    """
    parent_path = os.path.dirname(os.getcwd())
    files_path = os.path.join(parent_path, "data/restaurants_bars/*.json")
    json_files = glob.glob(files_path)
    data = []
    for file in json_files:
        with open(file, 'r', encoding='utf-8-sig') as f:
            data.append(json.load(f))
    return pd.DataFrame(data)