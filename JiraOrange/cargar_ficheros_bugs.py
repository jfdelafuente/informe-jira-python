import configD
import os
import json
import pandas as pd
import time
from utils.utils import load_to_csv, mostrar_bugs
from etl.transform import transform
from etl.parser import parsear_bugs

'''
    Proceso que consulta los fichero JSON de Incidencias almacenados en
    './JSON/BUGS para extraer y parsear los campos:
    
        - Incidencias
        - Bugs
        - Status
    
    en el fichero de salida 'bugs_out.csv'
    
'''   

def main():
    
    start_time = time.time()
    directorio = configD.DIR_JIRA_BUGS
    files = []
    # leemos los ficheros .json contenidos en el directorio de trabajo
    contenido = os.listdir(directorio)
    tam = len(contenido)
    print("Leemos %s ficheros." % (tam))
    for fichero in contenido:
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.json'):
            files.append(fichero)
    
    dict_metrics = {}
    df_salida = pd.DataFrame(dict_metrics, columns=['Incidencias','Bugs','Status','prj'])
    for file in files:
        print("Cargando ... %s " % file)
        with open(directorio + file) as archivo:
            datos = json.load(archivo)
            dict_metrics['Incidencias'], dict_metrics['Bugs'], dict_metrics['Status'], dict_metrics['prj'] = parsear_bugs(datos)
            new_salida = pd.DataFrame(dict_metrics)
            df_salida = pd.concat([df_salida, new_salida])
  
    df_filtrado = transform(df_salida)
    load_to_csv(configD.DIR_JIRA_OUT + 'bugs_out.csv', df_filtrado)

    mostrar_bugs(df_filtrado)
    print("COPY duration: {} seconds".format(time.time() - start_time))

if __name__ == '__main__':
    main()