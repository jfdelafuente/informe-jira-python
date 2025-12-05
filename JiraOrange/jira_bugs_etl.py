from utils.utils import log, load_to_csv, mostrar_bugs
from etl.extract import extract_bugs
from etl.transform import transform, Data_Quality, eliminar_duplicados
from etl.parser import parsear_bugs
import pandas as pd
import time


"""
Proceso ETL para bugs de Jira

Consulta los ficheros JSON de Incidencias almacenados en './JSON/BUGS'
para extraer y parsear los campos:
    - Incidencias
    - Bugs
    - Status

Genera el fichero de salida 'salida_bugs.csv'
"""

def main():
    """Ejecuta el proceso ETL completo para bugs"""
    start_time = time.time()

    try:
        # Fase de extracción
        log("Extract phase Started")
        extracted_data = extract_bugs()
        log("Extract phase Ended")

        # Fase de transformación
        log("Transform phase Started")
        extracted_data = eliminar_duplicados(extracted_data)
        dict_metrics = {}
        transformed_data = pd.DataFrame(dict_metrics, columns=['Incidencias', 'Bugs', 'Status'])

        for index, row in extracted_data.iterrows():
            dict_metrics['Incidencias'], dict_metrics['Bugs'], dict_metrics['Status'], dict_metrics['PRJ'] = parsear_bugs(row)
            new_salida = pd.DataFrame(dict_metrics, columns=['Incidencias', 'Bugs', 'Status'])
            transformed_data = pd.concat([transformed_data, new_salida])

        Data_Quality(transformed_data)
        df_filtrado = transform(transformed_data)
        log("Transform phase Ended")

        # Fase de carga
        log("Load phase Started")
        load_to_csv("salida_bugs.csv", df_filtrado)
        mostrar_bugs(df_filtrado)
        log("Load phase Ended")

        print("Proceso completado. Duración: {} seconds".format(time.time() - start_time))

    except Exception as e:
        log(f"Error en el proceso ETL: {e}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()