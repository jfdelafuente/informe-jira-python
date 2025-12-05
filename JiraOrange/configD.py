"""
Configuración de directorios del proyecto Jira
"""
import os
from pathlib import Path

# Directorio base del proyecto (un nivel arriba del módulo JiraOrange)
BASE_DIR = Path(__file__).parent.parent

# Directorios principales
DIR_JIRA = str(BASE_DIR) + '/'
DIR_JIRA_IN = str(BASE_DIR / 'in') + '/'
DIR_JIRA_OUT = str(BASE_DIR / 'out') + '/'
DIR_JIRA_DELIVS = str(BASE_DIR / 'JSON' / 'DELIVS') + '/'
DIR_JIRA_BUGS = str(BASE_DIR / 'JSON' / 'BUGS') + '/'

# Crear directorios si no existen
def _crear_directorios():
    """Crea los directorios necesarios si no existen"""
    directorios = [
        BASE_DIR / 'in',
        BASE_DIR / 'out',
        BASE_DIR / 'JSON' / 'DELIVS',
        BASE_DIR / 'JSON' / 'BUGS'
    ]
    for directorio in directorios:
        directorio.mkdir(parents=True, exist_ok=True)

# Ejecutar creación de directorios al importar el módulo
_crear_directorios()
