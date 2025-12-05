#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de validacion actualizado para la nueva estructura
Con colores para mejor visualizacion
"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Intentar importar colorama para colores en Windows
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)  # Auto-reset después de cada print
    HAS_COLORS = True
except ImportError:
    # Fallback sin colores si colorama no está instalado
    HAS_COLORS = False

    class Fore:
        GREEN = CYAN = YELLOW = RED = WHITE = MAGENTA = ""

    class Style:
        BRIGHT = RESET_ALL = DIM = ""

    class Back:
        GREEN = RED = ""


def print_header(text):
    """Imprime un encabezado con color"""
    if HAS_COLORS:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{text}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}")
    else:
        print(f"\n{'=' * 60}")
        print(text)
        print('=' * 60)


def print_section(text):
    """Imprime una sección con color"""
    if HAS_COLORS:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}[+] {text}{Style.RESET_ALL}")
    else:
        print(f"\n[+] {text}")


def print_ok(text):
    """Imprime mensaje de éxito con color verde"""
    if HAS_COLORS:
        print(f"   {Fore.GREEN}[OK]{Style.RESET_ALL} {text}")
    else:
        print(f"   [OK] {text}")


def print_fail(text):
    """Imprime mensaje de fallo con color rojo"""
    if HAS_COLORS:
        print(f"   {Fore.RED}[NO]{Style.RESET_ALL} {text}")
    else:
        print(f"   [NO] {text}")


def print_info(text):
    """Imprime mensaje informativo"""
    if HAS_COLORS:
        print(f"   {Fore.CYAN}{text}{Style.RESET_ALL}")
    else:
        print(f"   {text}")


def print_command(text):
    """Imprime un comando con color"""
    if HAS_COLORS:
        print(f"  {Fore.MAGENTA}{text}{Style.RESET_ALL}")
    else:
        print(f"  {text}")


def main():
    """Función principal de validación"""
    # Encabezado
    print_header("VALIDACION DEL ENTORNO - Jira ETL")

    if not HAS_COLORS:
        print_info("Nota: Instala 'colorama' para ver con colores (pip install colorama)")

    base_dir = Path(__file__).parent.parent
    all_ok = True

    # ========== Validar Python ==========
    print_section("Validando Python...")
    version = sys.version_info

    if version.major >= 3 and version.minor >= 8:
        print_ok(f"Python {version.major}.{version.minor}.{version.micro}")
    else:
        print_fail(f"Python {version.major}.{version.minor}.{version.micro} (requiere >= 3.8)")
        all_ok = False

    # ========== Validar estructura de directorios ==========
    print_section("Validando estructura de directorios...")

    dirs_nuevos = [
        ('src/jira_etl', 'Codigo fuente del paquete'),
        ('scripts', 'Scripts ejecutables'),
        ('data/input', 'Archivos de entrada'),
        ('data/output', 'Archivos de salida'),
        ('data/json/bugs', 'JSONs de bugs'),
        ('data/json/deliveries', 'JSONs de deliveries'),
        ('logs', 'Archivos de log'),
        ('tests', 'Tests del proyecto'),
        ('docs', 'Documentacion'),
    ]

    missing_dirs = []
    for d, desc in dirs_nuevos:
        path = base_dir / d
        exists = path.exists()
        if exists:
            print_ok(f"{d:<30} ({Fore.WHITE}{Style.DIM}{desc}{Style.RESET_ALL})")
        else:
            print_fail(f"{d:<30} - {Fore.RED}FALTA{Style.RESET_ALL}")
            missing_dirs.append(d)
            all_ok = False

    # ========== Validar archivos clave ==========
    print_section("Validando archivos clave...")

    files = [
        ('src/jira_etl/config.py', 'Configuracion'),
        ('scripts/extract_bugs.py', 'Extraccion bugs'),
        ('scripts/extract_deliveries.py', 'Extraccion deliveries'),
        ('scripts/run_full_etl.py', 'Pipeline completo'),
        ('pyproject.toml', 'Configuracion proyecto'),
        ('.env', 'Variables de entorno'),
    ]

    missing_files = []
    for f, desc in files:
        path = base_dir / f
        exists = path.exists()
        if exists:
            print_ok(f"{f:<35} ({Fore.WHITE}{Style.DIM}{desc}{Style.RESET_ALL})")
        else:
            print_fail(f"{f:<35} - {Fore.RED}FALTA{Style.RESET_ALL}")
            missing_files.append(f)
            if f != '.env':  # .env es opcional
                all_ok = False

    # ========== Validar variables de entorno ==========
    print_section("Validando variables de entorno...")

    from dotenv import load_dotenv
    load_dotenv()

    usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
    password = os.getenv('PASS') or os.getenv('PASSWORD')
    jira_host = os.getenv('JIRA_HOST', 'https://jira.si.orange.es')
    verify_ssl = os.getenv('JIRA_VERIFY_SSL', 'false')

    if usuario and password:
        print_ok(f"Credenciales configuradas")
        print_info(f"Usuario: {Fore.WHITE}{usuario}{Style.RESET_ALL}")
        print_info(f"Host: {Fore.WHITE}{jira_host}{Style.RESET_ALL}")
        print_info(f"Verificar SSL: {Fore.WHITE}{verify_ssl}{Style.RESET_ALL}")
    else:
        print_fail("Faltan credenciales en .env")
        print_info("Necesitas configurar USUARIO y PASS en el archivo .env")
        all_ok = False

    # ========== Validar dependencias (opcional) ==========
    print_section("Validando dependencias principales...")

    dependencies = [
        ('requests', 'Cliente HTTP'),
        ('pandas', 'Procesamiento de datos'),
        ('openpyxl', 'Lectura/escritura Excel'),
        ('python-dotenv', 'Variables de entorno'),
    ]

    for module, desc in dependencies:
        try:
            # Manejar nombres de módulos con guiones
            import_name = module.replace('-', '_').replace('python_', '')
            __import__(import_name)
            print_ok(f"{module:<25} ({Fore.WHITE}{Style.DIM}{desc}{Style.RESET_ALL})")
        except ImportError:
            print_fail(f"{module:<25} - {Fore.RED}NO INSTALADO{Style.RESET_ALL}")
            all_ok = False

    # ========== Resumen final ==========
    print()
    print("=" * 60)

    if all_ok:
        if HAS_COLORS:
            print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT} VALIDACION EXITOSA {Style.RESET_ALL}")
        else:
            print("[OK] VALIDACION EXITOSA")

        print()
        print_section("Siguientes pasos:")
        print_command(".\\run.ps1 extract-bugs      # Extraer bugs")
        print_command(".\\run.ps1 extract-delivs    # Extraer deliveries")
        print_command(".\\run.ps1 run-etl           # Pipeline completo")
        print()
        print_info("Documentacion: docs/README.md")
        print_info("Guia rapida: docs/guias/INICIO_RAPIDO.md")
    else:
        if HAS_COLORS:
            print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT} VALIDACION FALLIDA {Style.RESET_ALL}")
        else:
            print("[ERROR] VALIDACION FALLIDA")

        print()
        if missing_dirs:
            print_section("Directorios faltantes:")
            for d in missing_dirs:
                print_fail(d)

        if missing_files:
            print_section("Archivos faltantes:")
            for f in missing_files:
                print_fail(f)

        print()
        print_section("Solucion:")
        print_command(".\\run.ps1 setup             # Crear estructura")
        print_command("pip install -r requirements.txt  # Instalar dependencias")

        return 1

    print("=" * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
