import glob
import configD
import pandas as pd
from utils.utils import extract_from_json

def extract(file):
    extracted_data = pd.DataFrame() 
    for jsonfile in glob.glob(file):
        new_dataframe = extract_from_json(jsonfile)
        extracted_data = pd.concat([extracted_data, new_dataframe])

    return extracted_data

def extract_delivs():
    return extract(configD.DIR_JIRA_DELIVS + '/*.json')

def extract_bugs() -> pd.DataFrame:
    return extract(configD.DIR_JIRA_BUGS + "*.json")
   