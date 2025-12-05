"""Funciones de parseo de respuestas de Jira"""
import pandas as pd
from typing import Dict, List, Tuple
from ..utils.logger import get_logger

logger = get_logger(__name__)


def parsear_bugs(texto: dict) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Parsea la respuesta de Jira para extraer información de bugs.

    Args:
        texto: Diccionario con la respuesta de la API de Jira

    Returns:
        Tupla con 4 listas: (incidencias, bugs, status, proyectos)
    """
    if texto["maxResults"] > texto["total"]:
        contar = texto["total"]
    else:
        contar = texto["maxResults"]

    lista_inc = []
    lista_bug = []
    lista_status = []
    lista_resolution = []
    lista_prj = []

    if contar > 0:
        for j in range(0, contar):
            vNumIncidencia = texto["issues"][j]["fields"]["customfield_11104"]
            vIssueKey = texto["issues"][j]["key"]

            if vIssueKey != "":
                # Status
                if (texto["issues"][j]["fields"]["status"]) is not None:
                    vstatus = texto["issues"][j]["fields"]["status"]["name"]
                else:
                    vstatus = ""

                # Resolution
                if (texto["issues"][j]["fields"]["resolution"]) is not None:
                    vresolution = texto["issues"][j]["fields"]["resolution"]["name"]
                else:
                    vresolution = ""

                # Proyecto
                if (texto["issues"][j]["fields"]["customfield_14405"]) is not None:
                    prj = texto["issues"][j]["fields"]["customfield_14405"]["key"]
                else:
                    prj = ""

                vListaBugs = vIssueKey + " [ " + vstatus + " / " + vresolution + " ] "

                lista_inc.append(vNumIncidencia)
                lista_bug.append(vIssueKey)
                lista_prj.append(prj)
                lista_status.append(vstatus + " / " + vresolution)
                lista_resolution.append("")

    logger.debug(f"Parseados {len(lista_bug)} bugs")
    return lista_inc, lista_bug, lista_status, lista_prj


def parsear_delivs(datos: dict) -> List[dict]:
    """
    Parsea la respuesta de Jira para extraer información de deliveries.

    Args:
        datos: Diccionario con los datos de una delivery

    Returns:
        Lista de diccionarios con los datos parseados de cada delivery
    """
    total = len(datos["fields"]["customfield_16304"])
    logger.info(f"Total bugs: {total}")
    lista_delivs = []

    for i in range(total):
        dict_metrics = {}
        dict_metrics["issuekey"] = datos["key"]
        dict_metrics["status"] = datos["fields"]["status"]["name"]
        dict_metrics["resolution"] = datos["fields"]["customfield_16304"][i]["fields"]["status"]["name"]
        dict_metrics["created"] = datos["fields"]["created"]
        dict_metrics["updated"] = datos["fields"]["updated"]
        dict_metrics["resolution_date"] = datos["fields"]["resolutiondate"]
        dict_metrics["proveedor"] = datos["fields"]["customfield_18505"]
        dict_metrics["tipo"] = datos["fields"]["customfield_12107"][0]  # tipologia - 12107
        dict_metrics["prj"] = datos["fields"]["customfield_22300"][0]["key"]
        dict_metrics["remedy GGCC"] = datos["fields"]["customfield_11105"]
        dict_metrics["remedy HD"] = datos["fields"]["customfield_11104"]
        dict_metrics["summary"] = datos["fields"]["customfield_16304"][i]["fields"]["summary"]
        dict_metrics["bug"] = datos["fields"]["customfield_16304"][i]["key"]

        lista_delivs.append(dict_metrics)

    return lista_delivs
