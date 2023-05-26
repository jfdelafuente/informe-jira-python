import glob
import configD
import pandas as pd
from utils.utils import extract_from_json

def extract_bugs() -> pd.DataFrame:
    extracted_data = pd.DataFrame() 
    # for csv files
    # for csvfile in glob.glob("dealership_data/*.csv"):
    #     extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
    #for json files
    for jsonfile in glob.glob(configD.DIR_JIRA_BUGS + "*.json"):
        # extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
        new_salida = extract_from_json(jsonfile)
        extracted_data = pd.concat([ extracted_data, new_salida])
        
    return extracted_data
    
def extract_delivs() -> pd.DataFrame:
    extracted_data = pd.DataFrame() 
    #for csv files
    # for csvfile in glob.glob("dealership_data/*.csv"):
    #     extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
    #for json files
    for jsonfile in glob.glob(configD.DIR_JIRA_DELIVS + "*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
        
    return extracted_data
    
