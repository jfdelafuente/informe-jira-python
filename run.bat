@echo off
REM Script de utilidades para Windows CMD
REM Equivalente al Makefile para sistemas Unix

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="validate" goto validate
if "%1"=="run-etl" goto run-etl
if "%1"=="run" goto run-etl
if "%1"=="extract-bugs" goto extract-bugs
if "%1"=="extract-delivs" goto extract-delivs
if "%1"=="process-bugs" goto process-bugs
if "%1"=="process-delivs" goto process-delivs
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="install-package" goto install-package
if "%1"=="test" goto test
if "%1"=="test-auth" goto test-auth
if "%1"=="test-ssl" goto test-ssl
if "%1"=="clean" goto clean
if "%1"=="setup" goto setup
if "%1"=="init" goto setup
goto unknown

:help
echo.
echo ==================================================================
echo   Comandos Disponibles - Jira ETL Project
echo ==================================================================
echo.
echo Uso: run.bat ^<comando^>
echo.
echo COMANDOS PRINCIPALES:
echo   validate          Valida el entorno antes de ejecutar
echo   run-etl           Ejecuta el pipeline ETL completo
echo   run               Alias para run-etl
echo   extract-bugs      Extrae bugs desde Jira
echo   extract-delivs    Extrae deliveries desde Jira
echo   process-bugs      Procesa los bugs extraidos (ETL)
echo   process-delivs    Procesa las deliveries extraidas (ETL)
echo.
echo INSTALACION:
echo   install           Instala las dependencias del proyecto
echo   install-dev       Instala las dependencias de desarrollo
echo   install-package   Instala el paquete en modo editable
echo.
echo TESTING:
echo   test              Ejecuta los tests
echo   test-auth         Ejecuta test de autenticacion Jira
echo   test-ssl          Ejecuta test de conectividad SSL
echo.
echo UTILIDADES:
echo   clean             Limpia archivos temporales y cache
echo   setup / init      Setup inicial: crea directorios
echo   help              Muestra este mensaje de ayuda
echo.
echo ==================================================================
echo.
goto end

:validate
echo [+] Validando entorno...
python scripts\validate_environment.py
goto end

:run-etl
echo [+] Ejecutando pipeline ETL completo...
python scripts\run_full_etl.py
goto end

:extract-bugs
echo [+] Extrayendo bugs desde Jira...
python scripts\extract_bugs.py
goto end

:extract-delivs
echo [+] Extrayendo deliveries desde Jira...
python scripts\extract_deliveries.py
goto end

:process-bugs
echo [+] Procesando bugs...
python scripts\process_bugs.py
goto end

:process-delivs
echo [+] Procesando deliveries...
python scripts\process_deliveries.py
goto end

:install
echo [+] Instalando dependencias...
pip install -r requirements.txt
goto end

:install-dev
echo [+] Instalando dependencias de desarrollo...
pip install -r requirements.txt
if exist requirements-dev.txt (
    pip install -r requirements-dev.txt
)
goto end

:install-package
echo [+] Instalando paquete en modo editable...
pip install -e .
goto end

:test
echo [+] Ejecutando tests...
pytest tests\ -v
goto end

:test-auth
echo [+] Ejecutando test de autenticacion...
python tests\integration\test_jira_auth.py
goto end

:test-ssl
echo [+] Ejecutando test de SSL...
python tests\integration\test_jira_ssl.py
goto end

:clean
echo [+] Limpiando archivos temporales...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
if exist .pytest_cache rd /s /q .pytest_cache
if exist .mypy_cache rd /s /q .mypy_cache
if exist htmlcov rd /s /q htmlcov
if exist dist rd /s /q dist
if exist build rd /s /q build
if exist .coverage del /q .coverage
echo [OK] Limpieza completada
goto end

:setup
echo [+] Configurando entorno...
if not exist data\input mkdir data\input
if not exist data\output mkdir data\output
if not exist data\json\bugs mkdir data\json\bugs
if not exist data\json\deliveries mkdir data\json\deliveries
if not exist logs mkdir logs
echo [OK] Directorios creados

if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo [OK] Archivo .env creado desde .env.example
        echo [!] IMPORTANTE: Configura tus credenciales en .env
    ) else (
        echo [!] No se encontro .env.example
    )
) else (
    echo [OK] Archivo .env ya existe
)
echo [OK] Setup completado
goto end

:unknown
echo.
echo Comando desconocido: %1
echo.
goto help

:end
