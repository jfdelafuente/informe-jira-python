# 🔧 Parche para JiraAPIHandler.py

## Correcciones Mínimas Urgentes

Estas correcciones son **críticas** y se pueden aplicar en **5 minutos**.

---

## 1. Corregir typo `maxResult` → `maxResults`

### Línea 85
```python
# ANTES (❌ INCORRECTO)
'maxResult': '500'

# DESPUÉS (✅ CORRECTO)
'maxResults': 500  # Sin comillas, es un número
```

### Línea 100
```python
# ANTES (❌ INCORRECTO)
'maxResult': '500'

# DESPUÉS (✅ CORRECTO)
'maxResults': 500
```

### Línea 119
```python
# ANTES (❌ INCORRECTO)
'maxResult': '500'

# DESPUÉS (✅ CORRECTO)
'maxResults': 500
```

### Línea 130
```python
# ANTES (❌ INCORRECTO)
'maxResult': '500'

# DESPUÉS (✅ CORRECTO)
'maxResults': 500
```

---

## 2. Corregir bug en get_bug_to_json (línea 80-93)

### ANTES (❌ CON BUG)
```python
def get_bug_to_json(self, epsilon):
    query_args = {
        'jql': 'Type = Bug AND ("Remedy HD" ~ ' +epsilon+ ')',
        'fields': 'customfield_11104, issuetype, status, resolution, customfield_14405',
        'startAt' : '0',
        'maxResult': '500'
    }
    print(json.dumps(query_args, sort_keys=True, indent=4, separators=(",", ": ")))
    response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
    if response.status_code == 200:
        print("ok")
        bugs = json.loads(response.text)
        # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    return response.status_code, bugs  # ❌ bugs puede no estar definido
```

### DESPUÉS (✅ CORREGIDO)
```python
def get_bug_to_json(self, epsilon):
    query_args = {
        'jql': 'Type = Bug AND ("Remedy HD" ~ ' +epsilon+ ')',
        'fields': 'customfield_11104, issuetype, status, resolution, customfield_14405',
        'startAt' : 0,
        'maxResults': 500  # ✅ Corregido
    }
    # print removido o usar logging
    response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)

    bugs = None  # ✅ Inicializar variable
    if response.status_code == 200:
        bugs = response.json()  # ✅ Más limpio que json.loads(response.text)

    return response.status_code, bugs
```

---

## 3. Eliminar prints de debugging

### Línea 68 (eliminar)
```python
# ANTES
print(query_args)

# DESPUÉS
# print(query_args)  # Comentar o eliminar
```

### Línea 76 (eliminar)
```python
# ANTES
print(query_args)

# DESPUÉS
# print(query_args)  # Comentar o eliminar
```

### Línea 87 (eliminar)
```python
# ANTES
print(json.dumps(query_args, sort_keys=True, indent=4, separators=(",", ": ")))

# DESPUÉS
# print(json.dumps(query_args, sort_keys=True, indent=4, separators=(",", ": ")))
```

### Línea 90 (eliminar)
```python
# ANTES
print("ok")

# DESPUÉS
# Eliminar completamente esta línea
```

---

## 4. Agregar timeout (línea 55-61)

### ANTES
```python
response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth,
    params=query_args
)
```

### DESPUÉS
```python
response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth,
    params=query_args,
    timeout=30  # ✅ Agregar timeout de 30 segundos
)
```

---

## Archivo Completo con Correcciones Mínimas

```python
# Import the required libraries
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import os
from dotenv import load_dotenv
import json
import logging  # ✅ AGREGADO

# ✅ AGREGADO: Configurar logging
logger = logging.getLogger(__name__)

class JiraAPIHandler(object):
    """
    Adapter for JIRA web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'https://jira.si.orange.es'
    DEFAULT_BASE_PATH = ''

    # Endpoint for resources and rules
    JIRA_AUTH_ENDPOINT = '/rest/auth/1/session'
    JIRA_SEARCH_ENDPOINT = '/rest/api/latest/search'
    JIRA_ISSUE_SEARCH_ENDPOINT = '/rest/api/latest/issue'


    def __init__(self, host=None, port=None, base_path=None):
        load_dotenv()
        self._host = host or self.DEFAULT_HOST
        self._base_path = base_path or self.DEFAULT_BASE_PATH

        # Obtener credenciales con validación
        # Soporta tanto USUARIO/PASS como JIRA_USER/JIRA_PASSWORD
        self.usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
        self.password = os.getenv('PASS') or os.getenv('PASSWORD') or os.getenv('JIRA_PASSWORD')

        if not self.usuario or not self.password:
            raise ValueError(
                "Credenciales de Jira no configuradas. "
                "Define USUARIO y PASS en el archivo .env"
            )

    def _get_url(self, endpoint):
        return '{}{}{}'.format(self._host, self._base_path, endpoint)

    def _make_call(self, endpoint, **query_args):
        # Get method and make the call
        url = self._get_url(endpoint)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        auth = HTTPBasicAuth(self.usuario,
                             self.password)

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth,
            params=query_args,
            timeout=30  # ✅ AGREGADO
        )
        return response


    def get_issues(self, issue):
        query_args = {}
        logger.debug(f"Query args: {query_args}")  # ✅ CAMBIADO de print a logger
        body = self._make_call(self.JIRA_ISSUE_SEARCH_ENDPOINT + "/" + issue, **query_args)
        return body

    def get_project(self, proyecto):
        query_args = {
            'jql': 'project="' + proyecto + '"'
        }
        logger.debug(f"Query args: {query_args}")  # ✅ CAMBIADO
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body

    def get_bug_to_json(self, epsilon):
        query_args = {
            'jql': 'Type = Bug AND ("Remedy HD" ~ ' +epsilon+ ')',
            'fields': 'customfield_11104, issuetype, status, resolution, customfield_14405',
            'startAt' : 0,  # ✅ CAMBIADO: sin comillas
            'maxResults': 500  # ✅ CORREGIDO: era maxResult
        }
        logger.debug(f"Consultando bugs para {epsilon}")  # ✅ CAMBIADO
        response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)

        bugs = None  # ✅ AGREGADO: inicializar
        if response.status_code == 200:
            logger.info("Bugs obtenidos correctamente")  # ✅ CAMBIADO
            bugs = response.json()  # ✅ CAMBIADO: más limpio

        return response.status_code, bugs

    def get_bug(self, epsilon):
        query_args = {
            'jql': 'Type = Bug AND ("Remedy HD" ~ ' +epsilon+ ')',
            'fields': 'customfield_11104, issuetype, status, resolution',
            'startAt' : 0,  # ✅ CAMBIADO
            'maxResults': 500  # ✅ CORREGIDO
        }
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body

    def get_bugs(self, lista_epsilons):
        sJQL = "Type = Bug AND ("
        tam = len(lista_epsilons) -1
        for index, row in lista_epsilons.iterrows():
            if index < tam:
                sJQL += f' "Remedy HD" ~ {row["Incidencia"]} OR'
            else:
                sJQL += f' "Remedy HD" ~ {row["Incidencia"]}'
        sJQL += f' ) ORDER BY cf[11104], status ASC '
        query_args = {
            'jql': sJQL,  # ✅ SIMPLIFICADO: no necesita concatenar con ''
            'fields': 'customfield_11104, issuetype, status, resolution',
            'startAt' : 0,  # ✅ CAMBIADO
            'maxResults': 500  # ✅ CORREGIDO
        }
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body

    def get_delivs(self, sJQL):
        query_args = {
            'jql': sJQL,  # ✅ SIMPLIFICADO
            'fields' : 'issuekey, status, resolution, created, updated, resolutiondate, customfield_18505,customfield_12107,customfield_14405,customfield_22300,customfield_11105,customfield_11104,customfield_16304, customfield_16306, issue_actions',
            'startAt' : 0,  # ✅ CAMBIADO
            'maxResults': 500  # ✅ CORREGIDO
        }
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body
```

---

## Resumen de Cambios

| Línea(s) | Cambio | Tipo |
|----------|--------|------|
| 7 | Agregar `import logging` | Mejora |
| 10-11 | Configurar logger | Mejora |
| 61 | Agregar `timeout=30` | Crítico |
| 68 | `print` → `logger.debug` | Mejora |
| 76 | `print` → `logger.debug` | Mejora |
| 85 | `'maxResult'` → `maxResults` | Crítico |
| 85 | `'500'` → `500` | Importante |
| 87 | Eliminar o cambiar a logger | Mejora |
| 90 | Eliminar print("ok") | Mejora |
| 91 | `json.loads(response.text)` → `response.json()` | Mejora |
| 88 | Agregar `bugs = None` | Crítico |
| 100 | `'maxResult'` → `maxResults` | Crítico |
| 119 | `'maxResult'` → `maxResults` | Crítico |
| 130 | `'maxResult'` → `maxResults` | Crítico |

**Total de cambios críticos:** 5
**Total de cambios recomendados:** 7
**Tiempo estimado:** 5-10 minutos

---

## Cómo Aplicar

### Opción 1: Reemplazar archivo completo

```bash
# Hacer backup
cp JiraOrange/api/JiraAPIHandler.py JiraOrange/api/JiraAPIHandler.py.backup

# Usar versión mejorada
cp JiraOrange/api/JiraAPIHandler_mejorado.py JiraOrange/api/JiraAPIHandler.py
```

### Opción 2: Editar manualmente

1. Abre `JiraOrange/api/JiraAPIHandler.py`
2. Busca cada "maxResult" y cámbialo por "maxResults"
3. Cambia `'500'` por `500` (sin comillas)
4. Busca línea 61 y agrega `, timeout=30`
5. En línea 88, agregar `bugs = None` antes del if
6. Guarda el archivo

### Opción 3: Usar sed/awk (Linux/Mac)

```bash
cd JiraOrange/api

# Backup
cp JiraAPIHandler.py JiraAPIHandler.py.backup

# Aplicar correcciones
sed -i "s/'maxResult'/'maxResults'/g" JiraAPIHandler.py
sed -i "s/'maxResults': '500'/'maxResults': 500/g" JiraAPIHandler.py
sed -i "s/'startAt' : '0'/'startAt': 0/g" JiraAPIHandler.py
```

---

## Verificación

Después de aplicar los cambios, ejecuta:

```bash
# Verificar sintaxis
python -m py_compile JiraOrange/api/JiraAPIHandler.py

# Probar import
python -c "from JiraOrange.api.JiraAPIHandler import JiraAPIHandler; print('OK')"

# Ejecutar validación
python scripts/validate_environment.py
```

---

**Última actualización:** 2025-12-02
**Versión:** 1.0
