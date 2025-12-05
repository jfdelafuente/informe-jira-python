import pandas as pd
from utils.utils import load_to_csv, log
from etl.extract import extract_delivs
from etl.parser import parsear_delivs
from etl.transform import transform, Data_Quality


def main():
    extracted_delivs = extract_delivs()
    
    lista_delivs = []
    for index, row in extracted_delivs.iterrows():
        lista_delivs += parsear_delivs(row)

    transformed_data = pd.DataFrame(lista_delivs)
    # Data_Quality(transformed_data)    
    load_to_csv("salida_delivs.csv", transformed_data)

if __name__ == '__main__':
    main()
