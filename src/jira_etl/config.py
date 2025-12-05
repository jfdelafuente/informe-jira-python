"""
Configuración centralizada del proyecto Jira ETL
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """
    Clase de configuración centralizada para el proyecto Jira ETL.

    Maneja todos los paths, credenciales y configuraciones del proyecto.
    """

    # Directorio base del proyecto
    BASE_DIR = Path(__file__).parent.parent.parent

    # Directorios de datos
    DATA_DIR = BASE_DIR / 'data'
    INPUT_DIR = DATA_DIR / 'input'
    OUTPUT_DIR = DATA_DIR / 'output'
    JSON_DIR = DATA_DIR / 'json'

    # Directorios específicos
    BUGS_JSON_DIR = JSON_DIR / 'bugs'
    DELIVS_JSON_DIR = JSON_DIR / 'deliveries'
    BUGS_OUTPUT_DIR = OUTPUT_DIR / 'bugs'
    DELIVS_OUTPUT_DIR = OUTPUT_DIR / 'deliveries'

    # Directorio de logs
    LOGS_DIR = BASE_DIR / 'logs'

    # Archivos de entrada
    INPUT_FILE = INPUT_DIR / 'incidencias_in.csv'

    # Archivos de salida
    OUTPUT_BUGS_CSV = OUTPUT_DIR / 'salida_bugs.csv'
    OUTPUT_DELIVS_CSV = OUTPUT_DIR / 'salida_delivs.csv'

    # Configuración de Jira
    JIRA_HOST = os.getenv('JIRA_HOST', 'https://jira.si.orange.es')
    JIRA_USER = os.getenv('USUARIO') or os.getenv('JIRA_USER')
    JIRA_PASSWORD = os.getenv('PASS') or os.getenv('PASSWORD') or os.getenv('JIRA_PASSWORD')
    JIRA_VERIFY_SSL = os.getenv('JIRA_VERIFY_SSL', 'true').lower() not in ('false', '0', 'no')
    JIRA_TIMEOUT = int(os.getenv('JIRA_TIMEOUT', '30'))
    JIRA_MAX_RESULTS = int(os.getenv('JIRA_MAX_RESULTS', '100'))

    # Custom fields de Jira
    FIELD_REMEDY_HD = 'customfield_11104'
    FIELD_REMEDY_GGCC = 'customfield_11105'
    FIELD_TIPOLOGIA = 'customfield_12107'
    FIELD_PROJECT = 'customfield_14405'
    FIELD_BUGS = 'customfield_16304'
    FIELD_ENTORNOS = 'customfield_16306'
    FIELD_PROVEEDOR = 'customfield_18505'
    FIELD_PRJ_DELIV = 'customfield_22300'

    @classmethod
    def create_directories(cls) -> None:
        """Crea todos los directorios necesarios si no existen"""
        directories = [
            cls.INPUT_DIR,
            cls.OUTPUT_DIR,
            cls.BUGS_OUTPUT_DIR,
            cls.DELIVS_OUTPUT_DIR,
            cls.BUGS_JSON_DIR,
            cls.DELIVS_JSON_DIR,
            cls.LOGS_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> bool:
        """
        Valida que la configuración esté completa.

        Returns:
            True si la configuración es válida, False en caso contrario
        """
        if not cls.JIRA_USER or not cls.JIRA_PASSWORD:
            return False
        return True

    @classmethod
    def get_credentials(cls) -> tuple[Optional[str], Optional[str]]:
        """
        Obtiene las credenciales de Jira.

        Returns:
            Tupla (usuario, password)
        """
        return cls.JIRA_USER, cls.JIRA_PASSWORD


# Compatibilidad con código antiguo
DIR_JIRA = str(Config.BASE_DIR) + '/'
DIR_JIRA_IN = str(Config.INPUT_DIR) + '/'
DIR_JIRA_OUT = str(Config.OUTPUT_DIR) + '/'
DIR_JIRA_DELIVS = str(Config.DELIVS_JSON_DIR) + '/'
DIR_JIRA_BUGS = str(Config.BUGS_JSON_DIR) + '/'

# Crear directorios al importar
Config.create_directories()
