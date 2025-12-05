"""Utilidades para manejo de archivos"""
import pandas as pd
import json
from pathlib import Path
from .logger import get_logger

logger = get_logger(__name__)


def extract_from_csv(file_to_process: str) -> pd.DataFrame:
    """
    Extrae datos desde un archivo CSV.

    Args:
        file_to_process: Ruta del archivo CSV

    Returns:
        DataFrame con los datos del CSV
    """
    logger.info(f"Extrayendo datos desde CSV: {file_to_process}")
    dataframe = pd.read_csv(file_to_process)
    logger.info(f"Extraídas {len(dataframe)} filas")
    return dataframe


def extract_from_json(file_to_process: str) -> pd.DataFrame:
    """
    Extrae datos desde un archivo JSON.

    Args:
        file_to_process: Ruta del archivo JSON

    Returns:
        DataFrame con los datos del JSON
    """
    logger.debug(f"Extrayendo datos desde JSON: {file_to_process}")
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe


def extract_from_excel(file_to_process: str) -> pd.DataFrame:
    """
    Extrae datos desde un archivo Excel.

    Args:
        file_to_process: Ruta del archivo Excel

    Returns:
        DataFrame con los datos del Excel
    """
    logger.info(f"Extrayendo datos desde Excel: {file_to_process}")
    dataframe = pd.read_excel(file_to_process)
    logger.info(f"Extraídas {len(dataframe)} filas")
    return dataframe


def load_to_csv(targetfile: str, data_to_load: pd.DataFrame) -> None:
    """
    Carga datos a un archivo CSV.

    Args:
        targetfile: Ruta del archivo de destino
        data_to_load: DataFrame con los datos a guardar
    """
    logger.info(f"Guardando {len(data_to_load)} filas en CSV: {targetfile}")
    data_to_load.to_csv(targetfile, sep=';', encoding='utf-8', index=False)
    logger.info(f"Archivo CSV guardado exitosamente")


def load_to_json(targetfile: str, data_to_load: dict) -> None:
    """
    Carga datos a un archivo JSON.

    Args:
        targetfile: Ruta del archivo de destino
        data_to_load: Diccionario con los datos a guardar
    """
    logger.info(f"Guardando datos en JSON: {targetfile}")
    with open(targetfile, 'w', encoding='utf-8') as file:
        json.dump(data_to_load, file, ensure_ascii=False, indent=2)
    logger.info(f"Archivo JSON guardado exitosamente")


def mostrar_bugs(df: pd.DataFrame) -> str:
    """
    Formatea una lista de bugs para visualización.

    Args:
        df: DataFrame con columna 'Bugs'

    Returns:
        String formateado con la lista de bugs
    """
    string_lista_bug = ""
    count = 1
    for index, row in df.iterrows():
        if (count % 5 != 0):
            string_lista_bug = string_lista_bug + row['Bugs'] + ", "
        else:
            string_lista_bug = string_lista_bug + row['Bugs'] + ", "
            string_lista_bug = string_lista_bug + "\\\n"
        count = count + 1
    return string_lista_bug
