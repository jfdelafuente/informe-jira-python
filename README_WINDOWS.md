# Guía de Uso para Windows

Este documento explica cómo usar el proyecto en Windows sin necesidad de `make`.

## Scripts Disponibles

Se han creado dos scripts alternativos al Makefile:

### 1. PowerShell (Recomendado)

**Archivo:** `run.ps1`

**Uso:**
```powershell
.\run.ps1 <comando>
```

**Ejemplos:**
```powershell
# Ver ayuda
.\run.ps1 help

# Validar entorno
.\run.ps1 validate

# Ejecutar ETL completo
.\run.ps1 run-etl

# Extraer bugs
.\run.ps1 extract-bugs

# Limpiar archivos temporales
.\run.ps1 clean
```

### 2. Batch/CMD

**Archivo:** `run.bat`

**Uso:**
```cmd
run.bat <comando>
```

**Ejemplos:**
```cmd
REM Ver ayuda
run.bat help

REM Validar entorno
run.bat validate

REM Ejecutar ETL completo
run.bat run-etl
```

## Comandos Principales

### Setup Inicial

```powershell
# PowerShell
.\run.ps1 setup
```

```cmd
# CMD
run.bat setup
```

Este comando:
- Crea todos los directorios necesarios
- Copia `.env.example` a `.env` si no existe
- Prepara el entorno para trabajar

### Validar Entorno

```powershell
.\run.ps1 validate
```

Verifica que todo esté configurado correctamente antes de ejecutar.

### Ejecutar Pipeline ETL

```powershell
.\run.ps1 run-etl
```

Ejecuta el proceso completo de extracción, transformación y carga.

### Extraer Datos

```powershell
# Extraer bugs
.\run.ps1 extract-bugs

# Extraer deliveries
.\run.ps1 extract-delivs
```

### Procesar Datos

```powershell
# Procesar bugs
.\run.ps1 process-bugs

# Procesar deliveries
.\run.ps1 process-delivs
```

### Testing

```powershell
# Tests de autenticación
.\run.ps1 test-auth

# Tests de SSL
.\run.ps1 test-ssl

# Todos los tests (requiere pytest)
.\run.ps1 test
```

## Instalación de Dependencias

### 1. Dependencias de Producción

```powershell
.\run.ps1 install
```

### 2. Dependencias de Desarrollo

```powershell
.\run.ps1 install-dev
```

### 3. Instalar el Paquete

```powershell
.\run.ps1 install-package
```

## Limpieza

```powershell
.\run.ps1 clean
```

Elimina:
- Archivos `__pycache__`
- Archivos `.pyc` y `.pyo`
- Directorios de test (`.pytest_cache`, `.mypy_cache`)
- Archivos de cobertura
- Builds

## Solución de Problemas

### Error: No se puede ejecutar scripts de PowerShell

Si obtienes un error al ejecutar `.\run.ps1`, es probable que tengas que cambiar la política de ejecución:

```powershell
# Ver política actual
Get-ExecutionPolicy

# Cambiar política (ejecutar como Administrador)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Alternativa: Usar siempre .bat

Si no quieres o no puedes cambiar la política de PowerShell, simplemente usa `run.bat` en su lugar:

```cmd
run.bat validate
run.bat run-etl
```

## Comandos Python Directos

Si prefieres no usar los scripts, también puedes ejecutar los comandos directamente:

```powershell
# Validar
python scripts\validate_environment.py

# ETL completo
python scripts\run_full_etl.py

# Extraer bugs
python scripts\extract_bugs.py

# Extraer deliveries
python scripts\extract_deliveries.py

# Procesar bugs
python scripts\process_bugs.py

# Procesar deliveries
python scripts\process_deliveries.py

# Test de autenticación
python tests\integration\test_jira_auth.py

# Test de SSL
python tests\integration\test_jira_ssl.py
```

## Flujo de Trabajo Típico

1. **Primera vez:**
   ```powershell
   .\run.ps1 setup
   # Editar .env con tus credenciales
   .\run.ps1 install
   .\run.ps1 validate
   ```

2. **Uso diario:**
   ```powershell
   .\run.ps1 validate
   .\run.ps1 run-etl
   ```

3. **Desarrollo:**
   ```powershell
   .\run.ps1 install-dev
   .\run.ps1 test
   .\run.ps1 clean
   ```

## Notas

- Los scripts `run.ps1` y `run.bat` son funcionalmente equivalentes al `Makefile`
- Usa el que prefieras según tu entorno
- PowerShell ofrece mejor presentación con colores
- Batch/CMD funciona en cualquier versión de Windows sin configuración adicional

## Ver Todos los Comandos

```powershell
.\run.ps1 help
```

o

```cmd
run.bat help
```
