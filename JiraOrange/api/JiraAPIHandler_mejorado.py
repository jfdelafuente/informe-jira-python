"""
Cliente mejorado para la API de Jira

Este módulo proporciona una interfaz mejorada para interactuar con la API REST de Jira,
con manejo de errores, logging apropiado y mejores prácticas.

Mejoras sobre la versión original:
- ✅ Typo 'maxResult' → 'maxResults' corregido
- ✅ Manejo de errores robusto
- ✅ Logging en lugar de prints
- ✅ Type hints completos
- ✅ Docstrings en todos los métodos
- ✅ Timeout en requests
- ✅ Constantes para custom fields
- ✅ Código duplicado eliminado
"""

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, List, Tuple, Any

# Configurar logger
logger = logging.getLogger(__name__)


class JiraAPIHandler:
    """
    Cliente para interactuar con la API REST de Jira.

    Esta clase proporciona métodos para consultar issues, bugs y deliveries
    desde Jira usando autenticación básica HTTP.

    Attributes:
        DEFAULT_HOST: URL por defecto del servidor Jira
        DEFAULT_TIMEOUT: Timeout por defecto para peticiones HTTP (segundos)
        DEFAULT_MAX_RESULTS: Número máximo de resultados por página
    """

    # Configuración por defecto
    DEFAULT_HOST = 'https://jira.si.orange.es'
    DEFAULT_BASE_PATH = ''
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RESULTS = 100

    # Endpoints de la API
    JIRA_AUTH_ENDPOINT = '/rest/auth/1/session'
    JIRA_SEARCH_ENDPOINT = '/rest/api/latest/search'
    JIRA_ISSUE_SEARCH_ENDPOINT = '/rest/api/latest/issue'

    # Custom fields de Jira (documentados para claridad)
    FIELD_REMEDY_HD = 'customfield_11104'          # Número de incidencia Remedy HD
    FIELD_REMEDY_GGCC = 'customfield_11105'        # Remedy GGCC
    FIELD_TIPOLOGIA = 'customfield_12107'          # Tipología
    FIELD_PROJECT = 'customfield_14405'            # Proyecto
    FIELD_BUGS = 'customfield_16304'               # Bugs relacionados
    FIELD_ENTORNOS = 'customfield_16306'           # Entornos
    FIELD_PROVEEDOR = 'customfield_18505'          # Proveedor
    FIELD_PRJ_DELIV = 'customfield_22300'          # Proyecto delivery

    def __init__(
        self,
        host: Optional[str] = None,
        base_path: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        Inicializa el cliente de Jira.

        Args:
            host: URL del servidor Jira (opcional, usa DEFAULT_HOST si no se proporciona)
            base_path: Ruta base para los endpoints (opcional)
            timeout: Timeout para peticiones HTTP en segundos (opcional)

        Raises:
            ValueError: Si las credenciales no están configuradas en .env
        """
        load_dotenv()
        self._host = host or self.DEFAULT_HOST
        self._base_path = base_path or self.DEFAULT_BASE_PATH
        self._timeout = timeout or self.DEFAULT_TIMEOUT

        # Obtener credenciales con validación
        # Soporta tanto USUARIO/PASS como JIRA_USER/JIRA_PASSWORD
        self.usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
        self.password = os.getenv('PASS') or os.getenv('PASSWORD') or os.getenv('JIRA_PASSWORD')

        if not self.usuario or not self.password:
            raise ValueError(
                "Credenciales de Jira no configuradas. "
                "Define USUARIO y PASS en el archivo .env"
            )

        logger.info(f"Cliente Jira inicializado para {self._host}")

    def _get_url(self, endpoint: str) -> str:
        """
        Construye la URL completa para un endpoint.

        Args:
            endpoint: Endpoint de la API

        Returns:
            URL completa
        """
        return f'{self._host}{self._base_path}{endpoint}'

    def _make_call(
        self,
        endpoint: str,
        method: str = 'GET',
        **query_args
    ) -> requests.Response:
        """
        Realiza una llamada HTTP a la API de Jira.

        Args:
            endpoint: Endpoint de la API
            method: Método HTTP (GET, POST, etc.)
            **query_args: Parámetros de consulta

        Returns:
            Objeto Response de requests

        Raises:
            requests.RequestException: Si hay error en la petición HTTP
        """
        url = self._get_url(endpoint)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        auth = HTTPBasicAuth(self.usuario, self.password)

        logger.debug(f"Llamada {method} a {endpoint}")
        logger.debug(f"Parámetros: {query_args}")

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                auth=auth,
                params=query_args,
                timeout=self._timeout
            )
            response.raise_for_status()
            return response

        except requests.Timeout:
            logger.error(f"Timeout ({self._timeout}s) al conectar con {url}")
            raise
        except requests.RequestException as e:
            logger.error(f"Error en petición a {url}: {e}")
            raise

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Obtiene un issue específico por su clave.

        Args:
            issue_key: Clave del issue (ej: "PROJ-123")

        Returns:
            Diccionario con los datos del issue

        Raises:
            requests.RequestException: Si hay error en la petición
        """
        logger.info(f"Obteniendo issue: {issue_key}")
        endpoint = f"{self.JIRA_ISSUE_SEARCH_ENDPOINT}/{issue_key}"
        response = self._make_call(endpoint)
        return response.json()

    def get_project(self, project_key: str) -> Dict[str, Any]:
        """
        Obtiene todos los issues de un proyecto.

        Args:
            project_key: Clave del proyecto (ej: "MYPROJECT")

        Returns:
            Diccionario con los issues del proyecto

        Raises:
            requests.RequestException: Si hay error en la petición
        """
        logger.info(f"Obteniendo issues del proyecto: {project_key}")

        query_args = {
            'jql': f'project="{project_key}"',
            'maxResults': self.DEFAULT_MAX_RESULTS
        }

        response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return response.json()

    def get_bugs_by_remedy(
        self,
        remedy_id: str,
        fields: Optional[str] = None
    ) -> Tuple[int, Optional[Dict[str, Any]]]:
        """
        Obtiene bugs asociados a una incidencia Remedy HD.

        Args:
            remedy_id: Número de incidencia Remedy (ej: "INC000000012345")
            fields: Campos a obtener (opcional, usa campos por defecto si no se especifica)

        Returns:
            Tupla (status_code, data) donde:
            - status_code: Código HTTP de la respuesta
            - data: Diccionario con los bugs o None si hubo error
        """
        logger.info(f"Consultando bugs para Remedy HD: {remedy_id}")

        # Campos por defecto
        if not fields:
            fields = (
                f'{self.FIELD_REMEDY_HD}, '
                f'issuetype, '
                f'status, '
                f'resolution, '
                f'{self.FIELD_PROJECT}'
            )

        # Construir JQL
        jql = f'Type = Bug AND ("{self.FIELD_REMEDY_HD}" ~ {remedy_id})'

        query_args = {
            'jql': jql,
            'fields': fields,
            'startAt': 0,
            'maxResults': self.DEFAULT_MAX_RESULTS
        }

        try:
            response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
            data = response.json()

            total = data.get('total', 0)
            logger.info(f"Encontrados {total} bugs para {remedy_id}")

            return response.status_code, data

        except requests.RequestException as e:
            logger.error(f"Error consultando bugs para {remedy_id}: {e}")
            return 500, None

    def get_bugs_by_remedies(
        self,
        remedy_ids: List[str],
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtiene bugs asociados a múltiples incidencias Remedy HD.

        Args:
            remedy_ids: Lista de números de incidencia Remedy
            fields: Campos a obtener (opcional)

        Returns:
            Diccionario con los bugs encontrados

        Raises:
            requests.RequestException: Si hay error en la petición
        """
        logger.info(f"Consultando bugs para {len(remedy_ids)} incidencias")

        # Campos por defecto
        if not fields:
            fields = (
                f'{self.FIELD_REMEDY_HD}, '
                f'issuetype, '
                f'status, '
                f'resolution'
            )

        # Construir JQL con OR para múltiples incidencias
        conditions = [f'"{self.FIELD_REMEDY_HD}" ~ {rid}' for rid in remedy_ids]
        jql = f'Type = Bug AND ({" OR ".join(conditions)}) ORDER BY cf[11104], status ASC'

        query_args = {
            'jql': jql,
            'fields': fields,
            'startAt': 0,
            'maxResults': self.DEFAULT_MAX_RESULTS
        }

        response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return response.json()

    def get_deliveries(
        self,
        jql: str,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtiene deliveries usando una consulta JQL.

        Args:
            jql: Consulta JQL
            fields: Campos a obtener (opcional, usa campos por defecto si no se especifica)

        Returns:
            Diccionario con las deliveries encontradas

        Raises:
            requests.RequestException: Si hay error en la petición
        """
        logger.info("Consultando deliveries")

        # Campos por defecto para deliveries
        if not fields:
            fields = (
                f'issuekey, '
                f'status, '
                f'resolution, '
                f'created, '
                f'updated, '
                f'resolutiondate, '
                f'{self.FIELD_PROVEEDOR}, '
                f'{self.FIELD_TIPOLOGIA}, '
                f'{self.FIELD_PROJECT}, '
                f'{self.FIELD_PRJ_DELIV}, '
                f'{self.FIELD_REMEDY_GGCC}, '
                f'{self.FIELD_REMEDY_HD}, '
                f'{self.FIELD_BUGS}, '
                f'{self.FIELD_ENTORNOS}'
            )

        query_args = {
            'jql': jql,
            'fields': fields,
            'startAt': 0,
            'maxResults': self.DEFAULT_MAX_RESULTS
        }

        response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return response.json()

    def search(
        self,
        jql: str,
        fields: str = '*all',
        max_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Búsqueda genérica usando JQL.

        Args:
            jql: Consulta JQL
            fields: Campos a obtener (default: todos)
            max_results: Máximo de resultados (opcional)

        Returns:
            Diccionario con los resultados de la búsqueda

        Raises:
            requests.RequestException: Si hay error en la petición
        """
        logger.info(f"Búsqueda JQL: {jql[:100]}...")

        query_args = {
            'jql': jql,
            'fields': fields,
            'startAt': 0,
            'maxResults': max_results or self.DEFAULT_MAX_RESULTS
        }

        response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return response.json()


# Alias para compatibilidad con código existente
# Permite usar tanto el nombre antiguo como el nuevo
def get_bug(self, epsilon: str) -> requests.Response:
    """
    Método legacy para compatibilidad.

    DEPRECATED: Usar get_bugs_by_remedy() en su lugar.

    Args:
        epsilon: Número de incidencia

    Returns:
        Objeto Response
    """
    logger.warning("get_bug() está deprecated, usa get_bugs_by_remedy()")
    _, data = self.get_bugs_by_remedy(epsilon)
    # Crear un mock Response para compatibilidad
    response = requests.Response()
    response.status_code = 200 if data else 500
    response._content = str(data).encode()
    return response


# Agregar método legacy a la clase
JiraAPIHandler.get_bug = get_bug
