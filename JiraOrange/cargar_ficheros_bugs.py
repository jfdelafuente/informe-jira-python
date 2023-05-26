import configD
import os
import json
import pandas as pd
from utils.utils import load_to_csv, mostrar_bugs
from etl.transform import transform, transformar_bugs
   

def main():
    
    directorio = configD.DIR_JIRA_BUGS
    imagenes = []
    # leemos los ficheros .json contenidos en el directorio de trabajo
    contenido = os.listdir(directorio)
    tam = len(contenido)
    print("Leemos %s ficheros." % (tam))
    for fichero in contenido:
        if os.path.isfile(os.path.join(directorio, fichero)) and fichero.endswith('.json'):
            imagenes.append(fichero)
    
    dict_metrics = {}
    df_salida = pd.DataFrame(dict_metrics, columns=['Incidencias','Bugs','Status'])
    for images in imagenes:
        print("Cargando ... %s " % images)
        with open(directorio + images) as archivo:
            datos = json.load(archivo)
            dict_metrics['Incidencias'], dict_metrics['Bugs'], dict_metrics['Status'] = transformar_bugs(datos)
            new_salida = pd.DataFrame(dict_metrics)
            df_salida = pd.concat([df_salida, new_salida])

    
    df_filtrado = transform(df_salida)
    load_to_csv(configD.DIR_JIRA_OUT + 'bugs_out.csv', df_filtrado)

    mostrar_bugs(df_filtrado)

if __name__ == '__main__':
    main()