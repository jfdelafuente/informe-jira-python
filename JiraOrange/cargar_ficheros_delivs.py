import configD
import os
import json
import time
import pandas as pd
from utils.utils import load_to_csv
from etl.parser import parsear_delivs

'''
    Proceso que consulta los fichero JSON de DELIVs almacenados en
    './JSON/DELIVS para extraer y parsear los campos:
    
        - Incidencias
        - Bugs
        - Status
    
    en el fichero de salida 'data_delivs_jira.csv'
    
''' 

def main():
    start_time = time.time()
    directorio = configD.DIR_JIRA_DELIVS
    ficheros = []
    # leemos los ficheros .json contenidos en el directorio de trabajo
    contenido = os.listdir(directorio)
    tam = len(contenido)
    print("Leemos %s ficheros." % (tam))
    for fichero in contenido:
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.json'):
            ficheros.append(fichero)

    lista_delivs = []
    for file in ficheros:
        print("Cargando ... %s " % file)
        with open(directorio + file) as archivo:
            datos = json.load(archivo)
        lista_delivs += parsear_delivs(datos)
        # print(json.dumps(lista_delivs, sort_keys=True, indent=4, separators=(",", ": ")))

    df_salida = pd.DataFrame(lista_delivs)
    load_to_csv(configD.DIR_JIRA_OUT + 'data_delivs_jira.csv', df_salida)
    print("COPY duration: {} seconds".format(time.time() - start_time))
    


if __name__ == '__main__':
    main()
