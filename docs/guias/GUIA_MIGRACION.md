# Guía de Migración a la Nueva Estructura

## Resumen de Cambios

El proyecto ha sido reorganizado con una estructura moderna y profesional. Esta guía te ayudará a entender los cambios y cómo migrar tu flujo de trabajo.

## Estructura Antigua vs Nueva

### Antes

```plaintext
informe-jira-python/
├── JiraOrange/
│   ├── jira_bugs_to_json.py
│   ├── jira_delivs_to_json.py
│   ├── jira_bugs_etl.py
│   ├── jira_delivs_etl.py
│   ├── configD.py
│   ├── api/JiraAPIHandler.py
│   ├── etl/{extract,transform,parser}.py
│   └── utils/utils.py
├── in/                  # Archivos de entrada
├── out/                 # Archivos de salida
├── JSON/BUGS/
├── JSON/DELIVS/
└── validar_entorno.py
```

### Ahora

```plaintext
informe-jira-python/
├── src/jira_etl/              # Paquete Python instalable
│   ├── api/client.py          # JiraAPIHandler renombrado
│   ├── etl/                   # Módulos ETL
│   ├── utils/                 # Utilidades separadas
│   └── config.py              # Configuración centralizada
├── scripts/                   # Scripts ejecutables
│   ├── extract_bugs.py
│   ├── extract_deliveries.py
│   ├── process_bugs.py
│   ├── process_deliveries.py
│   ├── run_full_etl.py
│   └── validate_environment.py
├── data/                      # Datos organizados
│   ├── input/
│   ├── output/
│   └── json/{bugs,deliveries}/
├── tests/                     # Tests organizados
├── docs/                      # Documentación
├── config/                    # Configuración
└── logs/                      # Logs centralizados
```

## Mapeo de Archivos

| Antes | Ahora | Notas |
|-------|-------|-------|
| `JiraOrange/jira_bugs_to_json.py` | `scripts/extract_bugs.py` | Mejorado con logging |
| `JiraOrange/jira_delivs_to_json.py` | `scripts/extract_deliveries.py` | Mejorado con logging |
| `JiraOrange/jira_bugs_etl.py` | `scripts/process_bugs.py` | Mejorado con logging |
| `JiraOrange/jira_delivs_etl.py` | `scripts/process_deliveries.py` | Mejorado con logging |
| `JiraOrange/configD.py` | `src/jira_etl/config.py` | Configuración orientada a objetos |
| `JiraOrange/api/JiraAPIHandler.py` | `src/jira_etl/api/client.py` | Mantenido para compatibilidad |
| `JiraOrange/etl/` | `src/jira_etl/etl/` | Con imports actualizados |
| `JiraOrange/utils/utils.py` | `src/jira_etl/utils/` | Separado en múltiples módulos |
| `validar_entorno.py` | `scripts/validate_environment.py` | Movido a scripts |
| `in/` | `data/input/` | Renombrado para claridad |
| `out/` | `data/output/` | Renombrado para claridad |
| `JSON/BUGS/` | `data/json/bugs/` | Renombrado para claridad |
| `JSON/DELIVS/` | `data/json/deliveries/` | Renombrado para claridad |

## Comandos Antes vs Ahora

### Extracción de Bugs

**Antes:**
```bash
python JiraOrange/jira_bugs_to_json.py
```

**Ahora:**
```bash
# Opción 1: Con make
make extract-bugs

# Opción 2: Directamente
python scripts/extract_bugs.py
```

### Extracción de Deliveries

**Antes:**
```bash
python JiraOrange/jira_delivs_to_json.py
```

**Ahora:**
```bash
make extract-delivs
# o: python scripts/extract_deliveries.py
```

### Procesamiento de Bugs

**Antes:**
```bash
python JiraOrange/jira_bugs_etl.py
```

**Ahora:**
```bash
make process-bugs
# o: python scripts/process_bugs.py
```

### Procesamiento de Deliveries

**Antes:**
```bash
python JiraOrange/jira_delivs_etl.py
```

**Ahora:**
```bash
make process-delivs
# o: python scripts/process_deliveries.py
```

### Pipeline Completo (NUEVO)

```bash
make run-etl
# o: python scripts/run_full_etl.py
```

Este comando ejecuta todo el flujo automáticamente.

## Imports en el Código

### Antes

```python
import configD
import api.JiraAPIHandler as jiraAPIHandler
from utils.utils import extract_from_csv, load_to_json
from etl.extract import extract_bugs
from etl.transform import transform
```

### Ahora

```python
from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import extract_from_csv, load_to_json
from jira_etl.etl.extract import extract_bugs
from jira_etl.etl.transform import transform
```

## Configuración

### Antes (configD.py)

```python
DIR_JIRA = './'
DIR_JIRA_IN = DIR_JIRA + 'in/'
DIR_JIRA_OUT = DIR_JIRA + 'out/'
DIR_JIRA_BUGS = DIR_JIRA + 'JSON/BUGS/'
DIR_JIRA_DELIVS = DIR_JIRA + 'JSON/DELIVS/'
```

### Ahora (src/jira_etl/config.py)

```python
from jira_etl.config import Config

# Acceder a configuración
Config.INPUT_DIR
Config.OUTPUT_DIR
Config.BUGS_JSON_DIR
Config.DELIVS_JSON_DIR

# Variables de Jira
Config.JIRA_HOST
Config.JIRA_USER
Config.JIRA_PASSWORD
```

## Archivos de Entrada/Salida

### Ubicación de Archivos de Entrada

**Antes:**
```
in/incidencias_in.csv
```

**Ahora:**
```
data/input/incidencias_in.csv
```

### Ubicación de Archivos de Salida

**Antes:**
```
out/salida_bugs.csv
out/salida_delivs.csv
JSON/BUGS/*.json
JSON/DELIVS/*.json
```

**Ahora:**
```
data/output/salida_bugs.csv
data/output/salida_delivs.csv
data/json/bugs/*.json
data/json/deliveries/*.json
```

## Compatibilidad con Código Antiguo

Para facilitar la migración, se ha mantenido compatibilidad:

1. **Variables antiguas de configuración** siguen funcionando:
   ```python
   from jira_etl.config import DIR_JIRA, DIR_JIRA_IN, DIR_JIRA_OUT
   ```

2. **JiraAPIHandler** mantiene todos sus métodos originales

3. **Directorios legacy** (`in/`, `out/`, `JSON/`) aún se soportan

## Nuevas Características

### 1. Makefile

Comandos convenientes para tareas comunes:

```bash
make help              # Ver todos los comandos
make install           # Instalar dependencias
make validate          # Validar entorno
make run-etl           # Ejecutar pipeline completo
make clean             # Limpiar archivos temporales
make test              # Ejecutar tests
```

### 2. Logging Mejorado

Todos los scripts ahora generan logs en `logs/`:

```
logs/
├── extract_bugs_20250112_143022.log
├── process_bugs_20250112_144530.log
└── full_etl_pipeline_20250112_150000.log
```

### 3. pyproject.toml

Configuración moderna del proyecto:

```bash
# Instalar el paquete en modo desarrollo
pip install -e .

# Ahora puedes importar desde cualquier lugar
from jira_etl import Config, JiraClient
```

### 4. Tests Preparados

Estructura lista para agregar tests:

```
tests/
├── unit/           # Tests unitarios
├── integration/    # Tests de integración
└── fixtures/       # Datos de prueba
```

### 5. Script de Pipeline Completo

Ejecuta todo el flujo con un solo comando:

```bash
python scripts/run_full_etl.py
```

Esto ejecuta:
1. Extracción de bugs
2. Extracción de deliveries
3. Procesamiento de bugs
4. Procesamiento de deliveries

## Pasos para Migrar tu Código

### Si tienes scripts personalizados:

1. **Actualiza los imports:**
   ```python
   # Antiguo
   import configD
   from utils.utils import load_to_csv

   # Nuevo
   from jira_etl.config import Config
   from jira_etl.utils.file_utils import load_to_csv
   ```

2. **Actualiza las rutas:**
   ```python
   # Antiguo
   archivo = 'in/incidencias_in.csv'

   # Nuevo
   archivo = Config.INPUT_DIR / 'incidencias_in.csv'
   # o: archivo = 'data/input/incidencias_in.csv'
   ```

3. **Usa el nuevo logging:**
   ```python
   from jira_etl.utils.logger import setup_logging, get_logger

   setup_logging()
   logger = get_logger(__name__)
   logger.info("Mi mensaje")
   ```

## Migración de Datos

Para mover tus datos existentes a la nueva estructura:

```bash
# Copiar archivos de entrada
cp in/* data/input/

# Copiar JSONs de bugs
cp JSON/BUGS/* data/json/bugs/

# Copiar JSONs de deliveries
cp JSON/DELIVS/* data/json/deliveries/

# Copiar salidas
cp out/* data/output/
```

O usa el script de migración (si existe):

```bash
python scripts/migrate_data.py
```

## Verificación Post-Migración

Después de migrar, verifica que todo funciona:

```bash
# 1. Validar entorno
make validate

# 2. Probar con un pipeline completo
make run-etl

# 3. Verificar salidas
ls -la data/output/
```

## Rollback (Volver a la Versión Anterior)

Si necesitas volver a la estructura antigua:

```bash
git checkout HEAD~1  # O el commit antes de la migración
```

Los archivos antiguos se mantienen temporalmente para permitir una transición suave.

## Preguntas Frecuentes

**¿Necesito reinstalar las dependencias?**
No, las dependencias son las mismas. Pero se recomienda ejecutar:
```bash
pip install -r requirements.txt
```

**¿Mis archivos .env siguen funcionando?**
Sí, el archivo `.env` en la raíz del proyecto sigue siendo válido.

**¿Puedo seguir usando los comandos antiguos?**
Sí, los scripts antiguos en `JiraOrange/` siguen funcionando, pero se recomienda migrar a los nuevos.

**¿Dónde están ahora los logs?**
En el directorio `logs/` con nombres descriptivos y timestamps.

**¿Cómo ejecuto solo un paso específico?**
Usa los comandos make individuales: `make extract-bugs`, `make process-bugs`, etc.

## Soporte

Si tienes problemas con la migración:

1. Consulta esta guía
2. Revisa [DOCUMENTACION.md](DOCUMENTACION.md)
3. Crea un issue describiendo el problema

## Próximos Pasos

Una vez migrado, considera:

- [ ] Agregar tests para tu código personalizado
- [ ] Usar el Makefile para automatizar tareas
- [ ] Explorar los logs mejorados
- [ ] Contribuir mejoras al proyecto
