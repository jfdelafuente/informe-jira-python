# Jira ETL

> Pipeline ETL para extraer, transformar y cargar datos de bugs y deliveries desde Jira

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Descripción

**Jira ETL** es un pipeline completo que permite:

- ✅ **Extraer** bugs y deliveries desde Jira usando su API REST
- ✅ **Transformar** los datos aplicando filtros y validaciones
- ✅ **Cargar** los resultados en archivos CSV/Excel listos para análisis

Este proyecto está diseñado para automatizar el proceso de generación de informes desde Jira, facilitando el análisis y seguimiento de incidencias y entregas.

## Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd informe-jira-python

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Si tienes problemas en Windows (sin compilador C++):
# pip install -r requirements-compatible.txt
```

> 📖 **Nota:** Para más información sobre dependencias, consulta [REQUIREMENTS.md](REQUIREMENTS.md)

### 2. Configuración

```bash
# Copiar plantilla de configuración
cp config/.env.template .env

# Editar .env con tus credenciales
nano .env  # o usa tu editor favorito
```

Configura las siguientes variables en `.env`:

```env
USUARIO=tu_usuario_jira
PASS=tu_password_jira
JIRA_HOST=https://jira.si.orange.es
```

### 3. Preparar Datos de Entrada

Crea el archivo [data/input/incidencias_in.csv](data/input/incidencias_in.csv) con las incidencias a procesar:

```csv
Incidencia
INC000003088586
INC000003088592
```

### 4. Ejecutar Pipeline Completo

**En Linux/Mac:**
```bash
# Opción 1: Usando make (recomendado)
make run-etl

# Opción 2: Ejecutando el script directamente
python scripts/run_full_etl.py
```

**En Windows PowerShell:**
```powershell
# Opción 1: Usando el script run.ps1 (recomendado)
.\run.ps1 run-etl

# Opción 2: Ejecutando el script directamente
python scripts\run_full_etl.py
```

**En Windows CMD:**
```cmd
REM Opción 1: Usando run.bat (recomendado)
run.bat run-etl

REM Opción 2: Ejecutando el script directamente
python scripts\run_full_etl.py
```

> **Nota para Windows:** Si `make` no funciona, usa `run.ps1` (PowerShell) o `run.bat` (CMD). Ver [README_WINDOWS.md](README_WINDOWS.md) para más detalles.

¡Listo! Los resultados estarán en `data/output/`:

- `salida_bugs.csv` - Bugs procesados
- `salida_delivs.csv` - Deliveries procesadas

---

## Uso Avanzado

### Ejecutar Pasos Individuales

```bash
# Solo extracción de bugs
make extract-bugs
# o: python scripts/extract_bugs.py

# Solo procesamiento de bugs
make process-bugs
# o: python scripts/process_bugs.py

# Solo deliveries
make extract-delivs
make process-delivs
```

### Validar Entorno

Antes de ejecutar, valida que todo esté configurado correctamente:

```bash
make validate
# o: python scripts/validate_environment.py
```

### Comandos Disponibles

**En Linux/Mac (usando make):**

```bash
make help              # Muestra todos los comandos disponibles
make install           # Instala dependencias
make install-dev       # Instala dependencias de desarrollo
make test              # Ejecuta tests
make lint              # Verifica calidad del código
make format            # Formatea código automáticamente
make clean             # Limpia archivos temporales
make run-etl           # Ejecuta pipeline completo
make show-config       # Muestra configuración actual
```

**En Windows (usando run.ps1 o run.bat):**

```powershell
# PowerShell
.\run.ps1 help         # Muestra todos los comandos disponibles
.\run.ps1 install      # Instala dependencias
.\run.ps1 test-auth    # Test de autenticación
.\run.ps1 test-ssl     # Test de conectividad SSL
.\run.ps1 clean        # Limpia archivos temporales
.\run.ps1 run-etl      # Ejecuta pipeline completo

# CMD
run.bat help           # Muestra todos los comandos disponibles
run.bat validate       # Valida el entorno
run.bat run-etl        # Ejecuta pipeline completo
```

Ver [README_WINDOWS.md](README_WINDOWS.md) para documentación completa de Windows.

---

## Estructura del Proyecto

```plaintext
informe-jira-python/
├── src/jira_etl/           # Código fuente del paquete
│   ├── api/                # Cliente de Jira API
│   ├── etl/                # Pipeline ETL (extract, transform, load)
│   ├── utils/              # Utilidades y helpers
│   ├── models/             # Modelos de datos
│   ├── services/           # Servicios de negocio
│   └── config.py           # Configuración centralizada
│
├── scripts/                # Scripts ejecutables
│   ├── extract_bugs.py     # Extrae bugs desde Jira
│   ├── extract_deliveries.py
│   ├── process_bugs.py     # Procesa bugs (ETL)
│   ├── process_deliveries.py
│   └── run_full_etl.py     # Pipeline completo
│
├── data/                   # Datos del proyecto
│   ├── input/              # Archivos de entrada (CSV)
│   ├── output/             # Resultados (CSV/Excel)
│   └── json/               # JSONs intermedios
│       ├── bugs/
│       └── deliveries/
│
├── tests/                  # Tests automatizados
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── docs/                   # Documentación
│   ├── guias/
│   ├── arquitectura/
│   └── soluciones/
│
├── logs/                   # Archivos de log
├── config/                 # Archivos de configuración
├── .env                    # Variables de entorno (no versionado)
├── pyproject.toml          # Configuración del proyecto
├── Makefile                # Comandos útiles
└── README.md               # Este archivo
```

---

## Documentación Completa

### Guías de Usuario
- 📖 [Guía de Inicio Rápido](docs/guias/INICIO_RAPIDO.md)
- 🔧 [Guía de Instalación](docs/guias/SOLUCION_INSTALACION.md)
- ✅ [Guía de Validación](docs/guias/GUIA_VALIDACION.md)
- 🔄 [Guía de Migración](docs/guias/GUIA_MIGRACION.md)

### Documentación Técnica
- 📚 [Documentación Completa](docs/arquitectura/DOCUMENTACION.md)
- 🏗️ [Estructura del Proyecto](docs/arquitectura/ESTRUCTURA_NUEVA.md)
- 🔍 [Análisis de Jira API](docs/arquitectura/ANALISIS_JIRA_API_HANDLER.md)

### Soluciones y Troubleshooting
- 🛠️ [Solución SSL](docs/soluciones/SOLUCION_SSL.md)
- 🔐 [Solución SSL y Auth](docs/soluciones/SOLUCION_COMPLETA_SSL_Y_AUTH.md)
- 🩹 [Parche Jira API](docs/soluciones/PARCHE_JIRA_API_HANDLER.md)

### Changelog
- 📝 [Changelog de Mejoras](docs/CHANGELOG_MEJORAS.md)
- ✨ [Mejoras Implementadas](docs/MEJORAS_IMPLEMENTADAS.md)
- 🚀 [Mejoras Futuras](docs/MEJORAS_FUTURAS.md)

---

## Requisitos

- Python >= 3.8
- Acceso a la API de Jira
- Credenciales válidas de Jira

## Dependencias Principales

- `requests` - Cliente HTTP para Jira API
- `pandas` - Procesamiento y análisis de datos
- `python-dotenv` - Gestión de variables de entorno
- `colorama` - Colores en terminal (multiplataforma)
- `openpyxl` - Lectura/escritura de archivos Excel

📋 Ver [REQUIREMENTS.md](REQUIREMENTS.md) para guía completa de instalación y solución de problemas.

---

## Desarrollo

### Configurar Entorno de Desarrollo

```bash
# Instalar dependencias de desarrollo (incluye producción + dev tools)
pip install -r requirements-dev.txt

# O usando make (Linux/Mac)
make install-dev

# Instalar el paquete en modo editable
pip install -e .
```

> 📖 Consulta [REQUIREMENTS.md](REQUIREMENTS.md) para más opciones de instalación.

### Ejecutar Tests

```bash
# Ejecutar todos los tests
make test

# Con coverage
make test-cov
```

### Formatear Código

```bash
# Formatear automáticamente
make format

# Verificar formato sin modificar
make format-check
```

---

## Mejoras Implementadas

Esta versión incluye importantes mejoras sobre la versión original:

- ✅ **Estructura modular** - Código organizado en paquetes bien definidos
- ✅ **Configuración centralizada** - Toda la configuración en un solo lugar
- ✅ **Logging robusto** - Sistema de logs completo y configurable
- ✅ **Type hints** - Anotaciones de tipos para mejor soporte de IDE
- ✅ **Validación de datos** - Comprobaciones de calidad automáticas
- ✅ **Manejo de errores** - Gestión robusta de excepciones
- ✅ **Scripts mejorados** - Mensajes claros y códigos de salida apropiados
- ✅ **Testing** - Estructura preparada para tests automatizados
- ✅ **Documentación** - Docstrings completos y documentación organizada
- ✅ **Makefile** - Comandos convenientes para tareas comunes

Ver [CHANGELOG_MEJORAS.md](docs/CHANGELOG_MEJORAS.md) para más detalles.

---

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la [documentación](docs/arquitectura/DOCUMENTACION.md)
2. Consulta las [guías de solución de problemas](docs/soluciones/SOLUCION_SSL.md)
3. Crea un nuevo issue si es necesario

---

**¿Primera vez usando el proyecto?** → Comienza con la [Guía de Inicio Rápido](docs/guias/INICIO_RAPIDO.md)
