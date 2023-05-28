from utils.utils import log, load_to_csv, mostrar_bugs
from etl.extract import extract_bugs
from etl.transform import transform, Data_Quality
from etl.parser import parsear_bugs
import pandas as pd


def main():
    
    log("Extract phase Started")
    extracted_data = extract_bugs() 
    log("Extract phase Ended")
    
    log("Transform data")
    extracted_data.dropna()
    dict_metrics = {}
    transformed_data = pd.DataFrame(dict_metrics, columns=['Incidencias','Bugs','Status'])
    for index, row in extracted_data.iterrows():
        dict_metrics['Incidencias'], dict_metrics['Bugs'], dict_metrics['Status'] = parsear_bugs(row)
        new_salida = pd.DataFrame(dict_metrics, columns=['Incidencias','Bugs','Status'])
        transformed_data = pd.concat([transformed_data, new_salida])
    
    Data_Quality(transformed_data)    
    df_filtrado = transform(transformed_data)
    log("Transform phase Ended")
    
    log("Load phase Started")
    load_to_csv("salida_bugs.csv",df_filtrado)
    mostrar_bugs(df_filtrado)
    log("Load phase Ended")

if __name__ == '__main__':
    main()