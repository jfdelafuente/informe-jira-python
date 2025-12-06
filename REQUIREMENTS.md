# Guía de Dependencias del Proyecto

Este documento explica los diferentes archivos de requirements y cuándo usar cada uno.

## Archivos de Requirements

### 📦 `requirements.txt` (Recomendado)

**Propósito:** Dependencias principales para ejecutar el proyecto en producción.

**Usar cuando:**
- Instalas el proyecto por primera vez
- Despliegas a producción
- Solo necesitas ejecutar el ETL

**Instalación:**
```bash
pip install -r requirements.txt
```

**Dependencias incluidas:**
- `requests` - Cliente HTTP para Jira API
- `pandas` - Procesamiento de datos
- `python-dotenv` - Variables de entorno
- `colorama` - Colores en terminal (Windows compatible)
- `openpyxl` - Soporte Excel

---

### 🔧 `requirements-compatible.txt`

**Propósito:** Versión compatible para Windows sin compiladores C++.

**Usar cuando:**
- Trabajas en Windows sin Visual Studio Build Tools
- Tienes problemas instalando pandas 2.x
- Necesitas versiones más estables

**Instalación:**
```bash
pip install -r requirements-compatible.txt
```

**Diferencias clave:**
- Usa pandas 1.5.x en lugar de 2.x
- Incluye dependencias explícitas (numpy, pytz, python-dateutil)
- Rangos de versiones más conservadores

---

### 🛠️ `requirements-dev.txt`

**Propósito:** Dependencias de desarrollo, testing y calidad de código.

**Usar cuando:**
- Contribuyes al desarrollo del proyecto
- Ejecutas tests
- Necesitas herramientas de linting/formateo

**Instalación:**
```bash
pip install -r requirements-dev.txt
```

**Dependencias adicionales:**
- **Testing:** pytest, pytest-cov, pytest-mock
- **Formateo:** black, isort
- **Linting:** flake8, pylint
- **Type checking:** mypy + stubs
- Incluye automáticamente las de `requirements.txt`

---

## Instalación por Escenario

### Para Usuarios (Solo Ejecución)

```bash
# Opción 1: Instalación estándar (recomendado)
pip install -r requirements.txt

# Opción 2: Si tienes problemas en Windows
pip install -r requirements-compatible.txt
```

### Para Desarrolladores

```bash
# Instala todas las dependencias (producción + desarrollo)
pip install -r requirements-dev.txt

# Instala el paquete en modo editable
pip install -e .
```

### Actualizar Dependencias

```bash
# Actualizar solo las dependencias de producción
pip install --upgrade -r requirements.txt

# Actualizar todas las dependencias (desarrollo incluido)
pip install --upgrade -r requirements-dev.txt
```

---

## Verificar Instalación

Después de instalar, verifica que todo está correcto:

```bash
# Opción 1: Usar el script de validación
python scripts/validate_environment.py

# Opción 2: Con make (Linux/Mac)
make validate

# Opción 3: Con PowerShell (Windows)
.\run.ps1 validate

# Opción 4: Con CMD (Windows)
run.bat validate
```

---

## Solución de Problemas

### Error al instalar pandas

**Síntoma:**
```
ERROR: Could not build wheels for pandas
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solución:**
```bash
# Usa la versión compatible
pip install -r requirements-compatible.txt
```

### Conflictos de versiones

**Solución:**
```bash
# Crear un entorno virtual limpio
python -m venv venv_clean
source venv_clean/bin/activate  # Windows: venv_clean\Scripts\activate
pip install -r requirements.txt
```

### Verificar versiones instaladas

```bash
# Ver todas las dependencias
pip list

# Ver solo las principales
pip freeze | grep -E "(requests|pandas|dotenv|colorama|openpyxl)"
```

---

## Generar requirements.txt desde el entorno

Si necesitas actualizar los requirements basándote en tu entorno:

```bash
# Generar desde todas las instaladas
pip freeze > requirements-freeze.txt

# Luego edita manualmente para mantener solo las dependencias directas
```

---

## Notas Importantes

1. **No versionar el entorno virtual** - `.gitignore` ya lo excluye
2. **Versiones con rangos** - Usamos `>=X.Y,<Z.0` para permitir parches pero evitar breaking changes
3. **colorama es obligatorio** - Necesario para OutputManager en todos los scripts
4. **openpyxl es opcional** - Solo si trabajas con archivos Excel

---

## Dependencias por Categoría

### HTTP y API
- `requests` - Comunicación con Jira REST API

### Procesamiento de Datos
- `pandas` - Análisis y transformación de datos
- `numpy` - Dependencia de pandas
- `python-dateutil` - Manejo de fechas
- `pytz` - Zonas horarias

### Configuración
- `python-dotenv` - Carga de variables desde `.env`

### Terminal/UI
- `colorama` - Colores multiplataforma en consola

### Archivos
- `openpyxl` - Lectura/escritura de Excel

### Desarrollo (solo en dev)
- Testing, linting, formateo, type checking

---

Para más información, consulta la [documentación principal](README.md).
