# Nueva Estructura del Proyecto - Resumen Completo

## Estructura Completa del Proyecto

```plaintext
informe-jira-python/
│
├── src/jira_etl/                    # 📦 Paquete principal (código fuente)
│   ├── __init__.py
│   ├── __version__.py               # Versión del paquete
│   ├── config.py                    # ⚙️ Configuración centralizada
│   │
│   ├── api/                         # 🔌 Cliente API de Jira
│   │   ├── __init__.py
│   │   └── client.py                # JiraAPIHandler (renombrado)
│   │
│   ├── etl/                         # 🔄 Pipeline ETL
│   │   ├── __init__.py
│   │   ├── extract.py               # Extracción de datos
│   │   ├── transform.py             # Transformación de datos
│   │   └── parser.py                # Parseo de respuestas JSON
│   │
│   ├── models/                      # 📋 Modelos de datos (preparado)
│   │   └── __init__.py
│   │
│   ├── services/                    # 🛠️ Servicios de negocio (preparado)
│   │   └── __init__.py
│   │
│   └── utils/                       # 🔧 Utilidades
│       ├── __init__.py
│       ├── file_utils.py            # Operaciones con archivos
│       └── logger.py                # Sistema de logging
│
├── scripts/                         # 🚀 Scripts ejecutables
│   ├── extract_bugs.py              # Extrae bugs desde Jira → JSON
│   ├── extract_deliveries.py       # Extrae deliveries desde Jira → JSON
│   ├── process_bugs.py              # Procesa bugs: JSON → CSV
│   ├── process_deliveries.py       # Procesa deliveries: JSON → CSV
│   ├── run_full_etl.py              # Pipeline completo automático
│   └── validate_environment.py     # Valida configuración
│
├── data/                            # 📊 Datos del proyecto
│   ├── input/                       # Entrada: incidencias_in.csv
│   │   └── .gitkeep
│   ├── output/                      # Salida: CSVs procesados
│   │   ├── bugs/
│   │   ├── deliveries/
│   │   └── .gitkeep
│   └── json/                        # JSONs intermedios
│       ├── bugs/                    # Respuestas de Jira (bugs)
│       │   └── .gitkeep
│       └── deliveries/              # Respuestas de Jira (deliveries)
│           └── .gitkeep
│
├── tests/                           # ✅ Tests automatizados
│   ├── __init__.py
│   ├── conftest.py                  # Configuración de pytest
│   ├── unit/                        # Tests unitarios
│   │   └── __init__.py
│   ├── integration/                 # Tests de integración
│   │   └── __init__.py
│   └── fixtures/                    # Datos de prueba
│
├── docs/                            # 📚 Documentación organizada
│   ├── guias/                       # Guías de usuario
│   │   ├── inicio_rapido.md
│   │   ├── instalacion.md
│   │   └── validacion.md
│   ├── arquitectura/                # Documentación técnica
│   │   ├── estructura.md
│   │   └── analisis_api.md
│   └── soluciones/                  # Troubleshooting
│       ├── ssl.md
│       ├── auth.md
│       └── troubleshooting.md
│
├── logs/                            # 📝 Logs centralizados
│   ├── .gitkeep
│   └── README.md
│
├── config/                          # ⚙️ Archivos de configuración
│   └── .env.template                # Plantilla de configuración
│
├── JiraOrange/                      # ⚠️ Legacy (mantener temporalmente)
│   └── ...                          # Código antiguo para compatibilidad
│
├── in/                              # ⚠️ Legacy - usar data/input/
├── out/                             # ⚠️ Legacy - usar data/output/
├── JSON/                            # ⚠️ Legacy - usar data/json/
│
├── .env                             # 🔐 Variables de entorno (NO versionar)
├── .env.example                     # Ejemplo público de .env
├── .gitignore                       # Archivos a ignorar en Git
├── .editorconfig                    # Configuración del editor
│
├── pyproject.toml                   # 📦 Configuración moderna del proyecto
├── setup.py                         # Instalación del paquete
├── Makefile                         # 🛠️ Comandos útiles
│
├── requirements.txt                 # 📋 Dependencias de producción
├── requirements-dev.txt             # 📋 Dependencias de desarrollo
│
├── README.md                        # 📖 Documentación principal
├── CHANGELOG_MEJORAS.md             # Registro de cambios
├── GUIA_MIGRACION.md                # Guía de migración
├── ESTRUCTURA_NUEVA.md              # Este archivo
│
└── LICENSE                          # Licencia del proyecto
```

## Organización por Tipo de Contenido

### 📦 Código Fuente (`src/jira_etl/`)

Todo el código Python reutilizable está aquí, organizado en módulos:

- **api/** - Comunicación con Jira
- **etl/** - Lógica de extracción, transformación y carga
- **utils/** - Funciones auxiliares
- **models/** - Modelos de datos (futuro)
- **services/** - Lógica de negocio (futuro)

### 🚀 Scripts Ejecutables (`scripts/`)

Scripts que se ejecutan directamente desde la línea de comandos:

- **extract_*.py** - Extracción desde Jira
- **process_*.py** - Procesamiento ETL
- **run_full_etl.py** - Pipeline completo
- **validate_environment.py** - Validación

### 📊 Datos (`data/`)

Separación clara de entrada, salida y datos intermedios:

- **input/** - CSVs con incidencias a procesar
- **output/** - Resultados finales (CSVs)
- **json/** - Respuestas de Jira en formato JSON

### ✅ Tests (`tests/`)

Estructura para testing automatizado:

- **unit/** - Tests de componentes individuales
- **integration/** - Tests de flujo completo
- **fixtures/** - Datos de ejemplo para tests

### 📚 Documentación (`docs/`)

Documentación organizada por tipo:

- **guias/** - Tutoriales para usuarios
- **arquitectura/** - Documentación técnica
- **soluciones/** - Resolución de problemas

## Flujo de Datos

```
1. ENTRADA
   data/input/incidencias_in.csv
        ↓
2. EXTRACCIÓN
   scripts/extract_bugs.py
        ↓
   data/json/bugs/*.json
        ↓
3. TRANSFORMACIÓN
   scripts/process_bugs.py
        ↓
4. SALIDA
   data/output/salida_bugs.csv
```

## Comandos Principales

### Usando Make (Recomendado)

```bash
make help              # Ver todos los comandos
make validate          # Validar entorno
make extract-bugs      # Extraer bugs
make extract-delivs    # Extraer deliveries
make process-bugs      # Procesar bugs
make process-delivs    # Procesar deliveries
make run-etl           # Pipeline completo
make test              # Ejecutar tests
make clean             # Limpiar archivos temporales
```

### Usando Python Directamente

```bash
python scripts/extract_bugs.py
python scripts/extract_deliveries.py
python scripts/process_bugs.py
python scripts/process_deliveries.py
python scripts/run_full_etl.py
```

## Archivos de Configuración

### pyproject.toml

Configuración moderna del proyecto:
- Metadatos del paquete
- Dependencias
- Scripts de línea de comandos
- Configuración de herramientas (black, isort, mypy, pytest)

### Makefile

Comandos convenientes:
- Instalación de dependencias
- Ejecución de tests
- Formateo de código
- Limpieza de archivos

### .env

Variables de entorno:
- Credenciales de Jira
- Configuración del servidor
- Parámetros de conexión

## Beneficios de la Nueva Estructura

### 1. Separación de Responsabilidades

- **Código vs Datos** - Código en `src/`, datos en `data/`
- **Librería vs Scripts** - Paquete en `src/`, ejecutables en `scripts/`
- **Código vs Docs** - Documentación separada en `docs/`

### 2. Escalabilidad

- Fácil agregar nuevos módulos en `src/jira_etl/`
- Fácil agregar nuevos scripts en `scripts/`
- Preparado para crecer con `models/` y `services/`

### 3. Mantenibilidad

- Cada archivo tiene una responsabilidad clara
- Imports explícitos y bien organizados
- Configuración centralizada

### 4. Profesionalismo

- Sigue convenciones estándar de Python
- Estructura reconocible para otros desarrolladores
- Preparado para distribución como paquete

### 5. Testing

- Estructura clara para tests
- Separación unit/integration
- Fixtures reutilizables

### 6. Desarrollo

- Instalable en modo editable (`pip install -e .`)
- Comandos convenientes con Makefile
- Herramientas de calidad de código

## Comparación: Antes vs Ahora

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Organización** | Archivos mezclados | Separación clara por tipo |
| **Configuración** | Variables dispersas | Centralizada en `Config` |
| **Logging** | Prints y archivos manuales | Sistema robusto centralizado |
| **Scripts** | Dentro de JiraOrange/ | Directorio `scripts/` dedicado |
| **Datos** | in/, out/, JSON/ | `data/` con subdirectorios claros |
| **Tests** | No estructurados | Estructura profesional |
| **Docs** | Archivos .md sueltos | Organizada en `docs/` |
| **Instalación** | Solo requirements.txt | pyproject.toml + setup.py |
| **Comandos** | Python scripts largos | Makefile con aliases |

## Próximos Pasos Sugeridos

1. **Migrar scripts personalizados** - Ver [GUIA_MIGRACION.md](GUIA_MIGRACION.md)
2. **Agregar tests** - Usar estructura en `tests/`
3. **Documentar código nuevo** - Seguir estándar de docstrings
4. **Usar logging** - En lugar de prints
5. **Explorar Makefile** - Comandos convenientes

## Recursos

- **README principal**: [README.md](README.md)
- **Guía de migración**: [GUIA_MIGRACION.md](GUIA_MIGRACION.md)
- **Documentación completa**: [DOCUMENTACION.md](DOCUMENTACION.md)
- **Inicio rápido**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

---

**Creado:** Diciembre 2024
**Versión:** 1.0.0
**Estado:** ✅ Implementado
