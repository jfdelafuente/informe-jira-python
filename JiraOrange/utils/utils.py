from datetime import datetime
import pandas as pd
import json
import logging
import sys
from pathlib import Path

# Configurar logging
def setup_logging(log_file='jira_process.log', level=logging.INFO):
    """
    Configura el sistema de logging para el proyecto

    Args:
        log_file: Nombre del archivo de log
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Obtener logger para este módulo
logger = logging.getLogger(__name__)

def extract_from_csv(file_to_process) -> pd.DataFrame:
    """Extrae datos desde un archivo CSV"""
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    """Extrae datos desde un archivo JSON"""
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe

def extract_from_excel(file_to_process) -> pd.DataFrame:
    """Extrae datos desde un archivo Excel"""
    dataframe = pd.read_excel(file_to_process)
    return dataframe

def load_to_csv(targetfile, data_to_load):
    """Carga datos a un archivo CSV"""
    data_to_load.to_csv(targetfile, sep=';', encoding='utf-8', index=False)
    logger.info(f"Archivo CSV guardado: {targetfile}")

def load_to_json(targetfile, data_to_load):
    """Carga datos a un archivo JSON"""
    with open(targetfile, 'w', encoding='utf-8') as file:
        json.dump(data_to_load, file, ensure_ascii=False, indent=2)
    logger.info(f"Archivo JSON guardado: {targetfile}")

def log(message):
    """
    Función legacy de logging - mantiene compatibilidad con código antiguo
    Se recomienda usar el logger directamente en código nuevo
    """
    logger.info(message)
    # Mantener archivo legacy para compatibilidad
    timestamp_format = '%H:%M:%S-%h-%d-%Y'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("jira_bugs_logfile.txt", "a", encoding='utf-8') as f:
        f.write(timestamp + ',' + message + '\n')

def mostrar_bugs(df:pd.DataFrame):
    string_lista_bug = ""
    count = 1
    for index, row in df.iterrows():
        if (count % 5 != 0):
                string_lista_bug = string_lista_bug + row['Bugs'] + ", "
        else:
                string_lista_bug = string_lista_bug + row['Bugs'] + ", "
                string_lista_bug = string_lista_bug + "\\\n"
        count = count + 1
    print(string_lista_bug)


