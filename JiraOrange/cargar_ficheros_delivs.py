import configD
import os
import logging
import json
import pandas as pd
from utils.utils import load_to_csv, mostrar_bugs
from etl.transform import transformar_delivs

directorio = configD.DIR_JIRA_DELIVS
imagenes = []

def main():
    # leemos los ficheros .json contenidos en el directorio de trabajo
    contenido = os.listdir(directorio)
    tam = len(contenido)
    print("Leemos %s ficheros." % (tam))
    for fichero in contenido:
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.json'):
            imagenes.append(fichero)

    lista_delivs = []
    for images in imagenes:
        print("Cargando ... %s " % images)
        with open(directorio + images) as archivo:
            datos = json.load(archivo)
        lista_delivs += transformar_delivs(datos)
        print("------------------")
        # print(json.dumps(lista_delivs, sort_keys=True, indent=4, separators=(",", ": ")))

    df_salida = pd.DataFrame(lista_delivs)
    load_to_csv(configD.DIR_JIRA_OUT + 'data_delivs_jira.csv', df_salida)
    


if __name__ == '__main__':
    main()
