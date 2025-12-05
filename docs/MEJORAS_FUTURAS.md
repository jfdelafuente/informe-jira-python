# Mejoras Futuras - Informe Jira Python

Este documento detalla las mejoras recomendadas para continuar mejorando el proyecto, organizadas por prioridad.

---

## 🟡 Prioridad Media

### 1. Refactorizar funciones largas en `parser.py`

**Archivo:** [JiraOrange/etl/parser.py](JiraOrange/etl/parser.py)

**Problema:**
- La función `parsear_bugs()` tiene más de 40 líneas
- Maneja múltiples responsabilidades (validación, extracción, formateo)
- Difícil de testear y mantener

**Solución propuesta:**
```python
def parsear_bugs(texto: dict) -> tuple:
    """Parsea bugs del JSON de respuesta de Jira"""
    validar_respuesta(texto)
    cantidad = calcular_cantidad_a_procesar(texto)

    listas = {
        'inc': [], 'bug': [], 'status': [], 'prj': []
    }

    for i in range(cantidad):
        bug_data = extraer_datos_bug(texto["issues"][i])
        agregar_a_listas(listas, bug_data)

    return listas['inc'], listas['bug'], listas['status'], listas['prj']

def extraer_datos_bug(issue: dict) -> dict:
    """Extrae datos de un issue individual"""
    return {
        'incidencia': obtener_campo_seguro(issue, 'customfield_11104'),
        'key': issue['key'],
        'status': obtener_campo_seguro(issue, 'status', 'name'),
        'resolution': obtener_campo_seguro(issue, 'resolution', 'name'),
        'proyecto': obtener_campo_seguro(issue, 'customfield_14405', 'key')
    }

def obtener_campo_seguro(data: dict, *keys, default=''):
    """Obtiene un campo anidado de forma segura"""
    try:
        result = data
        for key in keys:
            result = result[key]
        return result if result is not None else default
    except (KeyError, TypeError):
        return default
```

**Beneficios:**
- Código más legible y modular
- Más fácil de testear
- Manejo de errores más claro
- Reutilizable

**Esfuerzo:** 2-3 horas
**Impacto:** Alto en mantenibilidad

---

### 2. Implementar paginación en consultas Jira

**Archivos afectados:**
- [JiraOrange/api/JiraAPIHandler.py](JiraOrange/api/JiraAPIHandler.py)
- [JiraOrange/jira_bugs_to_json.py](JiraOrange/jira_bugs_to_json.py)
- [JiraOrange/jira_delivs_to_json.py](JiraOrange/jira_delivs_to_json.py)

**Problema:**
- Límite actual de 500 resultados por consulta (`maxResult: 500`)
- Si hay más de 500 bugs/deliveries, se pierden datos
- No hay control de paginación automática

**Solución propuesta:**
```python
class JiraAPIHandler:

    def get_all_issues(self, jql: str, fields: str, batch_size: int = 100) -> list:
        """
        Obtiene todos los issues paginando automáticamente

        Args:
            jql: Query JQL
            fields: Campos a obtener
            batch_size: Tamaño de cada página (default 100)

        Returns:
            Lista completa de issues
        """
        all_issues = []
        start_at = 0

        while True:
            query_args = {
                'jql': jql,
                'fields': fields,
                'startAt': start_at,
                'maxResults': batch_size
            }

            response = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)

            if response.status_code != 200:
                raise Exception(f"Error en Jira API: {response.status_code}")

            data = response.json()
            issues = data.get('issues', [])
            all_issues.extend(issues)

            # Si obtenemos menos que batch_size, ya no hay más
            if len(issues) < batch_size:
                break

            start_at += batch_size
            print(f"Obtenidos {len(all_issues)} issues hasta ahora...")

        return all_issues

    def get_bug_to_json_paginated(self, epsilon: str) -> tuple:
        """Versión paginada de get_bug_to_json"""
        jql = f'Type = Bug AND ("Remedy HD" ~ {epsilon})'
        fields = 'customfield_11104, issuetype, status, resolution, customfield_14405'

        try:
            issues = self.get_all_issues(jql, fields)
            return 200, {'issues': issues, 'total': len(issues)}
        except Exception as e:
            return 500, {'error': str(e)}
```

**Uso:**
```python
# En jira_bugs_to_json.py
estatus, texto = jira.get_bug_to_json_paginated(row_inc)
```

**Beneficios:**
- No se pierden datos aunque haya >500 resultados
- Progreso visible con prints
- Más eficiente (tamaño de página configurable)

**Esfuerzo:** 3-4 horas
**Impacto:** Crítico si hay muchos datos

---

### 3. Agregar type hints completos

**Archivos:** Todos los `.py`

**Problema:**
- Type hints parciales o ausentes
- Dificulta el uso de IDEs y herramientas de análisis estático
- Más propenso a errores de tipos

**Solución propuesta:**
```python
from typing import Dict, List, Tuple, Optional
import pandas as pd

def extract_bugs() -> pd.DataFrame:
    """Extrae bugs desde archivos JSON"""
    ...

def parsear_bugs(texto: Dict) -> Tuple[List[str], List[str], List[str], List[str]]:
    """Parsea información de bugs"""
    ...

def load_to_csv(targetfile: str, data_to_load: pd.DataFrame) -> None:
    """Guarda DataFrame en CSV"""
    ...

class JiraAPIHandler:
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        base_path: Optional[str] = None
    ) -> None:
        ...

    def get_bug(self, epsilon: str) -> requests.Response:
        ...
```

**Herramientas recomendadas:**
- `mypy` - Verificador de tipos estático
- `pylance` - Extension de VS Code

**Beneficios:**
- Mejor autocompletado en IDEs
- Detección temprana de errores
- Documentación implícita

**Esfuerzo:** 2-3 horas
**Impacto:** Medio (calidad de código)

---

### 4. Mover JQL hardcodeado a configuración

**Archivo:** [JiraOrange/jira_delivs_to_json.py](JiraOrange/jira_delivs_to_json.py:23-30)

**Problema:**
- JQL con lista enorme de bugs hardcodeado en código
- Difícil de modificar sin tocar código
- No es reutilizable para otros proyectos

**Solución propuesta:**

**Crear:** `config/queries.yaml`
```yaml
# Consultas JQL predefinidas
queries:
  delivs_por_bugs:
    description: "Obtiene deliveries asociadas a bugs específicos"
    jql_template: 'type = Delivery AND "Bug/s" in ({bugs})'
    bugs_file: "config/bugs_list.txt"

  bugs_por_incidencia:
    description: "Bugs asociados a incidencia epsilon"
    jql_template: 'Type = Bug AND ("Remedy HD" ~ {incidencia})'

  todos_los_bugs:
    description: "Todos los bugs del proyecto"
    jql_template: 'Type = Bug AND project = {proyecto}'
```

**Crear:** `config/bugs_list.txt`
```
WCS-9489
INTEPS-14777
CRM4TE-22756
INTEPS-14788
...
```

**Modificar código:**
```python
import yaml

def cargar_query(nombre_query: str, **params) -> str:
    """Carga y formatea una query desde configuración"""
    with open('config/queries.yaml', 'r') as f:
        queries = yaml.safe_load(f)

    query_config = queries['queries'][nombre_query]

    # Si hay archivo de bugs, cargarlos
    if 'bugs_file' in query_config:
        with open(query_config['bugs_file'], 'r') as f:
            bugs = [line.strip() for line in f if line.strip()]
        params['bugs'] = ', '.join(bugs)

    return query_config['jql_template'].format(**params)

# Uso
sJQL = cargar_query('delivs_por_bugs')
```

**Beneficios:**
- Configuración externa (no tocar código)
- Queries reutilizables
- Fácil mantenimiento
- Versionable por separado

**Esfuerzo:** 2 horas
**Impacto:** Alto en mantenibilidad

---

## 🟢 Prioridad Baja

### 5. Crear tests unitarios

**Archivos nuevos:** `tests/`

**Problema:**
- No hay tests automatizados
- Refactorings arriesgados
- Dificil validar cambios

**Solución propuesta:**

**Estructura:**
```
tests/
├── __init__.py
├── test_api.py
├── test_extract.py
├── test_transform.py
├── test_parser.py
└── fixtures/
    ├── sample_bug.json
    └── sample_deliv.json
```

**Ejemplo:** `tests/test_transform.py`
```python
import pytest
import pandas as pd
from JiraOrange.etl.transform import eliminar_duplicados, transform, Data_Quality

class TestEliminarDuplicados:
    def test_elimina_duplicados_correctamente(self):
        # Arrange
        df = pd.DataFrame({
            'col1': [1, 2, 2, 3],
            'col2': ['a', 'b', 'b', 'c']
        })

        # Act
        resultado = eliminar_duplicados(df)

        # Assert
        assert len(resultado) == 3
        assert not resultado.duplicated().any()

    def test_dataframe_vacio(self):
        df = pd.DataFrame()
        resultado = eliminar_duplicados(df)
        assert resultado.empty

class TestTransform:
    def test_filtra_cancelled(self):
        df = pd.DataFrame({
            'Status': ['Open', "Cancelled / Won't Do", 'Closed']
        })
        resultado = transform(df)
        assert len(resultado) == 2
        assert "Cancelled / Won't Do" not in resultado['Status'].values

class TestDataQuality:
    def test_dataframe_vacio_retorna_false(self):
        df = pd.DataFrame()
        assert Data_Quality(df) == False

    def test_dataframe_con_nulls_lanza_excepcion(self):
        df = pd.DataFrame({'col': [1, None, 3]})
        with pytest.raises(Exception, match="Null values found"):
            Data_Quality(df)

    def test_dataframe_valido_retorna_true(self):
        df = pd.DataFrame({'col': [1, 2, 3]})
        assert Data_Quality(df) == True
```

**Ejecutar tests:**
```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=JiraOrange
```

**Beneficios:**
- Confianza en cambios
- Documentación viva
- Detección temprana de bugs
- CI/CD posible

**Esfuerzo:** 6-8 horas
**Impacto:** Muy alto (largo plazo)

---

### 6. Implementar consultas paralelas

**Problema:**
- Consultas secuenciales a Jira son lentas
- Si hay 100 incidencias, tarda 100 * tiempo_respuesta

**Solución propuesta:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

def procesar_incidencia(jira: JiraAPIHandler, row_inc: str, index: int) -> Tuple[bool, str, dict]:
    """Procesa una incidencia individual"""
    try:
        estatus, texto = jira.get_bug_to_json(row_inc)
        if estatus == 200:
            return True, row_inc, texto
        else:
            return False, row_inc, {'error': f'Status {estatus}'}
    except Exception as e:
        return False, row_inc, {'error': str(e)}

def procesar_incidencias_paralelo(
    jira: JiraAPIHandler,
    df_epsilons: pd.DataFrame,
    max_workers: int = 5
) -> List[Tuple[str, dict]]:
    """
    Procesa incidencias en paralelo

    Args:
        jira: Cliente Jira
        df_epsilons: DataFrame con incidencias
        max_workers: Máximo de threads paralelos

    Returns:
        Lista de tuplas (nombre_archivo, datos)
    """
    resultados = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Enviar todas las tareas
        futures = {
            executor.submit(procesar_incidencia, jira, row['Incidencia'], index): index
            for index, row in df_epsilons.iterrows()
        }

        # Procesar conforme terminan
        for future in as_completed(futures):
            index = futures[future]
            try:
                exito, row_inc, texto = future.result()
                if exito:
                    log(f"Tratado {index+1} - {row_inc} - Estado: 200")
                    resultados.append((row_inc + "_bugs_new.json", texto))
                else:
                    log(f"Error {index+1} - {row_inc} - {texto.get('error')}")
            except Exception as e:
                log(f"Excepción procesando índice {index}: {e}")

    return resultados

# Uso en main()
resultados = procesar_incidencias_paralelo(jira, df_epsilons, max_workers=5)
for nom_fichero, texto in resultados:
    load_to_json(configD.DIR_JIRA_BUGS + nom_fichero, texto)
```

**Beneficios:**
- 5-10x más rápido con 5 workers
- Mejor uso de recursos
- Tiempo de ejecución reducido drásticamente

**Precauciones:**
- No saturar servidor Jira (limitar workers)
- Manejar rate limiting
- Logs thread-safe

**Esfuerzo:** 4-5 horas
**Impacto:** Muy alto en rendimiento

---

### 7. Renombrar carpeta "JiraOrange"

**Problema:**
- Nombre poco descriptivo
- No sigue convenciones (debería ser minúsculas)

**Solución propuesta:**
```bash
# Opción 1: Nombre genérico
JiraOrange/ → src/

# Opción 2: Nombre descriptivo
JiraOrange/ → jira_etl/

# Opción 3: Nombre del proyecto
JiraOrange/ → informe_jira/
```

**Cambios necesarios:**
- Renombrar carpeta
- Actualizar imports en todos los archivos
- Actualizar README
- Actualizar .gitignore si es necesario

**Beneficios:**
- Mejor semántica
- Sigue convenciones Python (PEP 8)
- Más profesional

**Esfuerzo:** 1 hora
**Impacto:** Bajo (estético)

---

### 8. Agregar CLI con argumentos

**Problema:**
- Parámetros hardcodeados (archivo CSV, directorios)
- No se puede reutilizar fácilmente

**Solución propuesta:**

**Crear:** `JiraOrange/cli.py`
```python
import argparse
from pathlib import Path
from jira_bugs_to_json import procesar_bugs
from jira_delivs_to_json import procesar_delivs
from jira_bugs_etl import ejecutar_etl_bugs

def main():
    parser = argparse.ArgumentParser(
        description='Herramienta ETL para Jira'
    )

    subparsers = parser.add_subparsers(dest='comando', help='Comando a ejecutar')

    # Comando: extract-bugs
    extract_bugs = subparsers.add_parser(
        'extract-bugs',
        help='Extrae bugs desde Jira'
    )
    extract_bugs.add_argument(
        '-i', '--input',
        default='incidencias_in.csv',
        help='Archivo CSV con incidencias'
    )
    extract_bugs.add_argument(
        '-o', '--output',
        default='JSON/BUGS',
        help='Directorio de salida'
    )

    # Comando: extract-delivs
    extract_delivs = subparsers.add_parser(
        'extract-delivs',
        help='Extrae deliveries desde Jira'
    )
    extract_delivs.add_argument(
        '--query-file',
        help='Archivo con query JQL'
    )

    # Comando: etl
    etl = subparsers.add_parser(
        'etl',
        help='Ejecuta proceso ETL completo'
    )
    etl.add_argument(
        'tipo',
        choices=['bugs', 'delivs', 'all'],
        help='Tipo de ETL a ejecutar'
    )
    etl.add_argument(
        '--output',
        default='.',
        help='Directorio de salida'
    )

    args = parser.parse_args()

    # Ejecutar comando
    if args.comando == 'extract-bugs':
        procesar_bugs(args.input, args.output)
    elif args.comando == 'extract-delivs':
        procesar_delivs(args.query_file)
    elif args.comando == 'etl':
        if args.tipo in ['bugs', 'all']:
            ejecutar_etl_bugs(args.output)
        if args.tipo in ['delivs', 'all']:
            ejecutar_etl_delivs(args.output)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

**Uso:**
```bash
# Extraer bugs
python -m JiraOrange.cli extract-bugs -i mis_incidencias.csv

# ETL completo
python -m JiraOrange.cli etl all --output ./resultados

# Ver ayuda
python -m JiraOrange.cli --help
```

**Beneficios:**
- Más flexible y reutilizable
- Documentación integrada (--help)
- Scripts más profesionales
- Fácil de automatizar

**Esfuerzo:** 3-4 horas
**Impacto:** Medio (usabilidad)

---

## 📊 Matriz de Prioridades

| Mejora | Prioridad | Esfuerzo | Impacto | ROI |
|--------|-----------|----------|---------|-----|
| 1. Refactorizar parser | Media | 2-3h | Alto | ⭐⭐⭐⭐ |
| 2. Paginación Jira | Media | 3-4h | Crítico | ⭐⭐⭐⭐⭐ |
| 3. Type hints | Media | 2-3h | Medio | ⭐⭐⭐ |
| 4. JQL a config | Media | 2h | Alto | ⭐⭐⭐⭐ |
| 5. Tests unitarios | Baja | 6-8h | Muy Alto | ⭐⭐⭐⭐⭐ |
| 6. Consultas paralelas | Baja | 4-5h | Muy Alto | ⭐⭐⭐⭐⭐ |
| 7. Renombrar carpeta | Baja | 1h | Bajo | ⭐⭐ |
| 8. CLI con argumentos | Baja | 3-4h | Medio | ⭐⭐⭐ |

---

## 🎯 Roadmap Recomendado

### Fase 1 (Semana 1-2) - Quick Wins
1. ✅ Mover JQL a configuración (2h)
2. ✅ Implementar paginación (4h)
3. ✅ Refactorizar parser (3h)

**Total:** ~9 horas
**Beneficio:** Código más limpio, sin pérdida de datos

### Fase 2 (Semana 3-4) - Calidad
4. ✅ Agregar type hints (3h)
5. ✅ Crear tests básicos (6h)
6. ✅ Renombrar a estructura estándar (1h)

**Total:** ~10 horas
**Beneficio:** Mejor calidad de código, tests iniciales

### Fase 3 (Mes 2) - Performance
7. ✅ Consultas paralelas (5h)
8. ✅ CLI con argumentos (4h)
9. ✅ Ampliar suite de tests (4h)

**Total:** ~13 horas
**Beneficio:** Mucho más rápido, mejor UX

---

## 🔗 Enlaces Útiles

- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [pytest Documentation](https://docs.pytest.org/)
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)
- [argparse Tutorial](https://docs.python.org/3/howto/argparse.html)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

---

## 📝 Notas

- Estas mejoras son **opcionales** - el proyecto ya funciona bien
- Prioriza según tus necesidades reales
- Implementa incrementalmente, no todo a la vez
- Haz tests manuales después de cada mejora
- Considera crear una rama por cada mejora importante

---

**Última actualización:** 2025-12-02
**Estado del proyecto:** Funcional y mantenible con mejoras de alta prioridad completadas
