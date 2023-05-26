from utils.utils import log
import pandas as pd

def transform(data:pd.DataFrame) -> pd.DataFrame:
    df_filtrado = data[data["Status"]!= "Cancelled / Won't Do"]
    return df_filtrado

'''
Funcion que vuelca al fichero tres campos: NumIncidencia, Bug y Status/Resolucion
'''
def transformar_bugs(texto:dict):
    if texto["maxResults"] > texto["total"]:
        contar = texto["total"]
    else:
        contar = texto["maxResults"]

    lista_inc = []
    lista_bug = []
    lista_status = []
    lista_resolution = []
    
    if contar > 0:
        for j in range(0, contar):
            vNumIncidencia = texto["issues"][j]["fields"]["customfield_11104"]
            vIssueKey = texto["issues"][j]["key"]
            # print("%s - vIssueKey:  %s - vNumIncidencia:  %s" %  (j, vIssueKey, vNumIncidencia))
            if vIssueKey != "":
                if (texto["issues"][j]["fields"]["status"]) is not None:
                    vstatus = texto["issues"][j]["fields"]["status"]["name"]
                else:
                    vstatus = ""
                if (texto["issues"][j]["fields"]["resolution"]) is not None:
                    vresolution = texto["issues"][j]["fields"]["resolution"]["name"]
                else:
                    vresolution = ""
                vListaBugs = vIssueKey + " [ " + vstatus + " / " + vresolution + " ] "
                # print("%s - vIssueKey:  %s - vNumIncidencia:  %s - vListaBugs: %s" %  (j, vIssueKey, vNumIncidencia, vListaBugs))
                lista_inc.append(vNumIncidencia)
                lista_bug.append(vIssueKey)
                lista_status.append(vstatus+ " / " +vresolution)
                # lista_status.append(vstatus)
                # lista_resolution.append(vresolution)
                lista_resolution.append("")
        
    return lista_inc, lista_bug, lista_status

