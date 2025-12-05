"""Funciones de extracción de datos"""
import glob
from pathlib import Path
import pandas as pd
from ..config import Config
from ..utils.file_utils import extract_from_json


def extract(file_pattern: str) -> pd.DataFrame:
    """
    Extrae datos de archivos JSON según un patrón.

    Args:
        file_pattern: Patrón de búsqueda de archivos (glob pattern)

    Returns:
        DataFrame con todos los datos extraídos
    """
    extracted_data = pd.DataFrame()
    for jsonfile in glob.glob(file_pattern):
        new_dataframe = extract_from_json(jsonfile)
        extracted_data = pd.concat([extracted_data, new_dataframe])

    return extracted_data


def extract_delivs() -> pd.DataFrame:
    """
    Extrae datos de deliveries desde archivos JSON.

    Returns:
        DataFrame con los datos de deliveries
    """
    pattern = str(Config.DELIVS_JSON_DIR / '*.json')
    return extract(pattern)


def extract_bugs() -> pd.DataFrame:
    """
    Extrae datos de bugs desde archivos JSON.

    Returns:
        DataFrame con los datos de bugs
    """
    pattern = str(Config.BUGS_JSON_DIR / '*.json')
    return extract(pattern)
