"""
Jira ETL - Pipeline para extraer, transformar y cargar datos de Jira

Este paquete proporciona herramientas para extraer información de bugs y deliveries
desde Jira, transformarla y cargarla en archivos CSV/Excel.
"""
from .config import Config
from .api.client import JiraAPIHandler
from .__version__ import __version__

# Alias para compatibilidad
JiraClient = JiraAPIHandler

__all__ = ['Config', 'JiraAPIHandler', 'JiraClient', '__version__']
