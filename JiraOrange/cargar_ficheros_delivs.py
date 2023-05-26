import configD
import os
import logging
import json
import pandas as pd
from utils.utils import load, mostrar_bugs

directorio = configD.DIR_JIRA_DELIVS
imagenes = []
lista_delivs = []


def parsear_datos(datos):
    total = len(datos["fields"]["customfield_16304"])
    print("Total bugs %s " % total)
    lista_delivs = []

    for i in range(total):
        dict_metrics = {}
        dict_metrics["issuekey"] = datos["key"]  # key
        dict_metrics["status"] = datos["fields"]["status"]["name"]  # status
        dict_metrics["resolution"] = datos["fields"]["customfield_16304"][i]["fields"]["status"]["name"]
        dict_metrics["created"] = datos["fields"]["created"]  # created
        dict_metrics["updated"] = datos["fields"]["updated"]  # updated
        dict_metrics["resolution_date"] = datos["fields"]["resolutiondate"]     
        dict_metrics["proveedor"] = datos["fields"]["customfield_18505"]
        dict_metrics["tipo"] = datos["fields"]["customfield_12107"][0] # tipologia - 12107
        dict_metrics["prj"] = datos["fields"]["customfield_22300"][0]["key"]
        dict_metrics["remedy GGCC"] = datos["fields"]["customfield_11105"]
        dict_metrics["remedy HD"] = datos["fields"]["customfield_11104"]
        dict_metrics["summary"] = datos["fields"]["customfield_16304"][i]["fields"]["summary"]
        dict_metrics["bug"] = datos["fields"]["customfield_16304"][i]["key"]

        lista_delivs.append(dict_metrics)
        # print(json.dumps(lista_delivs, sort_keys=True, indent=4, separators=(",", ": ")))

    return lista_delivs


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
            '''
            lista_inc, lista_bug, lista_status = parsear_datos(datos)
            dict_metrics['Incidencias'] = lista_inc
            dict_metrics['Bugs'] = lista_bug
            dict_metrics['Status'] = lista_status
            new_salida = pd.DataFrame(dict_metrics)
            df_salida = pd.concat([df_salida, new_salida])
            '''
        lista_delivs += parsear_datos(datos)
        print("------------------")
        # print(json.dumps(lista_delivs, sort_keys=True, indent=4, separators=(",", ": ")))

    df_salida = pd.DataFrame(lista_delivs)
    nom_excel = configD.DIR_JIRA_OUT + 'data_delivs_jira.csv'
    # df_salida.to_csv(nom_excel, sep=';', encoding='utf-8', index=False)
    load(nom_excel, df_salida)
    


if __name__ == '__main__':
    main()
