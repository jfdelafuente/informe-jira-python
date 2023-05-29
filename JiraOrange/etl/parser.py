from utils.utils import log
import pandas as pd

'''
Funcion que vuelca al fichero tres campos: NumIncidencia, Bug y Status/Resolucion
'''
def parsear_bugs(texto:dict):
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

def parsear_delivs(datos:dict):
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
        # dict_metrics["entornos"] = datos["fields"]["customfield_16306"]

        lista_delivs.append(dict_metrics)
        # print(json.dumps(lista_delivs, sort_keys=True, indent=4, separators=(",", ": ")))

    return lista_delivs