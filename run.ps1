# Script de utilidades para Windows PowerShell
# Equivalente al Makefile para sistemas Unix

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host "  Comandos Disponibles - Jira ETL Project" -ForegroundColor Cyan
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\run.ps1 <comando>" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "COMANDOS PRINCIPALES:" -ForegroundColor Green
    Write-Host "  validate          Valida el entorno antes de ejecutar" -ForegroundColor White
    Write-Host "  run-etl           Ejecuta el pipeline ETL completo" -ForegroundColor White
    Write-Host "  extract-bugs      Extrae bugs desde Jira" -ForegroundColor White
    Write-Host "  extract-delivs    Extrae deliveries desde Jira" -ForegroundColor White
    Write-Host "  process-bugs      Procesa los bugs extraidos (ETL)" -ForegroundColor White
    Write-Host "  process-delivs    Procesa las deliveries extraidas (ETL)" -ForegroundColor White
    Write-Host ""
    Write-Host "INSTALACION:" -ForegroundColor Green
    Write-Host "  install           Instala las dependencias del proyecto" -ForegroundColor White
    Write-Host "  install-dev       Instala las dependencias de desarrollo" -ForegroundColor White
    Write-Host "  install-package   Instala el paquete en modo editable" -ForegroundColor White
    Write-Host ""
    Write-Host "TESTING:" -ForegroundColor Green
    Write-Host "  test              Ejecuta los tests" -ForegroundColor White
    Write-Host "  test-auth         Ejecuta test de autenticacion Jira" -ForegroundColor White
    Write-Host "  test-ssl          Ejecuta test de conectividad SSL" -ForegroundColor White
    Write-Host "  test-cov          Ejecuta los tests con cobertura" -ForegroundColor White
    Write-Host ""
    Write-Host "CALIDAD DE CODIGO:" -ForegroundColor Green
    Write-Host "  lint              Verifica el codigo con flake8" -ForegroundColor White
    Write-Host "  format            Formatea el codigo con black e isort" -ForegroundColor White
    Write-Host "  format-check      Verifica el formato sin modificar" -ForegroundColor White
    Write-Host ""
    Write-Host "UTILIDADES:" -ForegroundColor Green
    Write-Host "  clean             Limpia archivos temporales y cache" -ForegroundColor White
    Write-Host "  setup             Setup inicial: crea directorios" -ForegroundColor White
    Write-Host "  show-config       Muestra la configuracion actual" -ForegroundColor White
    Write-Host "  help              Muestra este mensaje de ayuda" -ForegroundColor White
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Invoke-Validate {
    Write-Host "[+] Validando entorno..." -ForegroundColor Cyan
    python scripts/validate_environment.py
}

function Invoke-RunETL {
    Write-Host "[+] Ejecutando pipeline ETL completo..." -ForegroundColor Cyan
    python scripts/run_full_etl.py
}

function Invoke-ExtractBugs {
    Write-Host "[+] Extrayendo bugs desde Jira..." -ForegroundColor Cyan
    python scripts/extract_bugs.py
}

function Invoke-ExtractDelivs {
    Write-Host "[+] Extrayendo deliveries desde Jira..." -ForegroundColor Cyan
    python scripts/extract_deliveries.py
}

function Invoke-ProcessBugs {
    Write-Host "[+] Procesando bugs..." -ForegroundColor Cyan
    python scripts/process_bugs.py
}

function Invoke-ProcessDelivs {
    Write-Host "[+] Procesando deliveries..." -ForegroundColor Cyan
    python scripts/process_deliveries.py
}

function Invoke-Install {
    Write-Host "[+] Instalando dependencias..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

function Invoke-InstallDev {
    Write-Host "[+] Instalando dependencias de desarrollo..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if (Test-Path "requirements-dev.txt") {
        pip install -r requirements-dev.txt
    }
}

function Invoke-InstallPackage {
    Write-Host "[+] Instalando paquete en modo editable..." -ForegroundColor Cyan
    pip install -e .
}

function Invoke-Test {
    Write-Host "[+] Ejecutando tests..." -ForegroundColor Cyan
    pytest tests/ -v
}

function Invoke-TestAuth {
    Write-Host "[+] Ejecutando test de autenticacion..." -ForegroundColor Cyan
    python tests/integration/test_jira_auth.py
}

function Invoke-TestSSL {
    Write-Host "[+] Ejecutando test de SSL..." -ForegroundColor Cyan
    python tests/integration/test_jira_ssl.py
}

function Invoke-TestCov {
    Write-Host "[+] Ejecutando tests con cobertura..." -ForegroundColor Cyan
    pytest tests/ -v --cov=src/jira_etl --cov-report=html --cov-report=term
}

function Invoke-Lint {
    Write-Host "[+] Verificando codigo..." -ForegroundColor Cyan
    flake8 src/ scripts/ --max-line-length=100 --exclude=__pycache__,*.pyc,.git
}

function Invoke-Format {
    Write-Host "[+] Formateando codigo..." -ForegroundColor Cyan
    black src/ scripts/ tests/
    isort src/ scripts/ tests/
}

function Invoke-FormatCheck {
    Write-Host "[+] Verificando formato..." -ForegroundColor Cyan
    black --check src/ scripts/ tests/
    isort --check-only src/ scripts/ tests/
}

function Invoke-Clean {
    Write-Host "[+] Limpiando archivos temporales..." -ForegroundColor Cyan

    # Limpiar __pycache__
    Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

    # Limpiar archivos .pyc y .pyo
    Get-ChildItem -Path . -File -Recurse -Include "*.pyc", "*.pyo" | Remove-Item -Force

    # Limpiar directorios de test y build
    $dirsToRemove = @(".pytest_cache", ".mypy_cache", "htmlcov", "dist", "build", ".coverage")
    foreach ($dir in $dirsToRemove) {
        if (Test-Path $dir) {
            Remove-Item -Path $dir -Recurse -Force
            Write-Host "  [OK] Eliminado: $dir" -ForegroundColor Green
        }
    }

    # Limpiar .egg-info
    Get-ChildItem -Path . -Directory -Recurse -Filter "*.egg-info" | Remove-Item -Recurse -Force

    Write-Host "[OK] Limpieza completada" -ForegroundColor Green
}

function Invoke-Setup {
    Write-Host "[+] Configurando entorno..." -ForegroundColor Cyan

    # Crear directorios necesarios
    python -c "from pathlib import Path; dirs = ['data/input', 'data/output', 'data/json/bugs', 'data/json/deliveries', 'logs']; [Path(d).mkdir(parents=True, exist_ok=True) for d in dirs]; print('[OK] Directorios creados')"

    # Copiar .env.example si no existe .env
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Host "[OK] Archivo .env creado desde .env.example" -ForegroundColor Yellow
            Write-Host "[!] IMPORTANTE: Configura tus credenciales en .env" -ForegroundColor Yellow
        } else {
            Write-Host "[!] No se encontro .env.example" -ForegroundColor Red
        }
    } else {
        Write-Host "[OK] Archivo .env ya existe" -ForegroundColor Green
    }

    Write-Host "[OK] Setup completado" -ForegroundColor Green
}

function Invoke-ShowConfig {
    Write-Host "[+] Mostrando configuracion actual..." -ForegroundColor Cyan
    python -c @"
import os
from dotenv import load_dotenv
load_dotenv()

print('')
print('Configuracion:')
print(f'  JIRA_HOST: {os.getenv(\"JIRA_HOST\", \"https://jira.si.orange.es\")}')
print(f'  JIRA_USER: {os.getenv(\"USUARIO\") or os.getenv(\"JIRA_USER\") or \"<no configurado>\"}')
print(f'  JIRA_VERIFY_SSL: {os.getenv(\"JIRA_VERIFY_SSL\", \"false\")}')
print('')
"@
}

# Ejecutar comando
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "validate" { Invoke-Validate }
    "run-etl" { Invoke-RunETL }
    "run" { Invoke-RunETL }  # Alias
    "extract-bugs" { Invoke-ExtractBugs }
    "extract-delivs" { Invoke-ExtractDelivs }
    "process-bugs" { Invoke-ProcessBugs }
    "process-delivs" { Invoke-ProcessDelivs }
    "install" { Invoke-Install }
    "install-dev" { Invoke-InstallDev }
    "install-package" { Invoke-InstallPackage }
    "test" { Invoke-Test }
    "test-auth" { Invoke-TestAuth }
    "test-ssl" { Invoke-TestSSL }
    "test-cov" { Invoke-TestCov }
    "lint" { Invoke-Lint }
    "check" { Invoke-Lint }  # Alias
    "format" { Invoke-Format }
    "fmt" { Invoke-Format }  # Alias
    "format-check" { Invoke-FormatCheck }
    "clean" { Invoke-Clean }
    "setup" { Invoke-Setup }
    "init" { Invoke-Setup }  # Alias
    "show-config" { Invoke-ShowConfig }
    default {
        Write-Host ""
        Write-Host "Comando desconocido: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}
