#!/usr/bin/env python3
"""
Script de validación del entorno del proyecto Informe Jira Python

Verifica que todos los requisitos estén satisfechos antes de ejecutar:
- Versión de Python
- Librerías instaladas
- Variables de entorno configuradas
- Estructura de directorios
- Archivos de entrada disponibles
- Conectividad con Jira

Uso:
    python validar_entorno.py
    python validar_entorno.py --verbose
    python validar_entorno.py --skip-jira  # Omite prueba de conexión
"""

import sys
import os
from pathlib import Path
import importlib
import argparse
from typing import List, Tuple, Dict

# Colores para terminal
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Imprime encabezado de sección"""
    print(f"\n{Color.BOLD}{Color.BLUE}{'=' * 60}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{text.center(60)}{Color.END}")
    print(f"{Color.BOLD}{Color.BLUE}{'=' * 60}{Color.END}\n")

def print_check(test_name: str, passed: bool, message: str = "", warning: bool = False):
    """Imprime resultado de una validación"""
    if passed:
        symbol = f"{Color.GREEN}[OK]{Color.END}"
        status = f"{Color.GREEN}OK{Color.END}"
    elif warning:
        symbol = f"{Color.YELLOW}[!]{Color.END}"
        status = f"{Color.YELLOW}ADVERTENCIA{Color.END}"
    else:
        symbol = f"{Color.RED}[X]{Color.END}"
        status = f"{Color.RED}ERROR{Color.END}"

    print(f"{symbol} {test_name:<45} [{status}]")
    if message:
        print(f"  -> {message}")

# ============================================================================
# VALIDACIONES
# ============================================================================

def validar_version_python() -> Tuple[bool, str]:
    """Verifica que la versión de Python sea >= 3.7"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 7:
        return True, f"Python {version_str}"
    else:
        return False, f"Python {version_str} - Se requiere Python 3.7 o superior"

def validar_librerias() -> Tuple[bool, List[str], List[str]]:
    """Verifica que todas las librerías requeridas estén instaladas"""
    librerias_requeridas = {
        'requests': 'requests',
        'pandas': 'pandas',
        'dotenv': 'python-dotenv',
        'openpyxl': 'openpyxl'
    }

    instaladas = []
    faltantes = []

    for lib_import, lib_nombre in librerias_requeridas.items():
        try:
            importlib.import_module(lib_import)
            instaladas.append(lib_nombre)
        except ImportError:
            faltantes.append(lib_nombre)

    return len(faltantes) == 0, instaladas, faltantes

def validar_estructura_directorios() -> Tuple[bool, Dict[str, bool]]:
    """Verifica que existan todos los directorios necesarios"""
    base_dir = Path(__file__).parent

    directorios = {
        'JiraOrange/': base_dir / 'JiraOrange',
        'JiraOrange/api/': base_dir / 'JiraOrange' / 'api',
        'JiraOrange/etl/': base_dir / 'JiraOrange' / 'etl',
        'JiraOrange/utils/': base_dir / 'JiraOrange' / 'utils',
        'in/': base_dir / 'in',
        'out/': base_dir / 'out',
        'JSON/': base_dir / 'JSON',
        'JSON/BUGS/': base_dir / 'JSON' / 'BUGS',
        'JSON/DELIVS/': base_dir / 'JSON' / 'DELIVS',
    }

    estado = {}
    todos_existen = True

    for nombre, ruta in directorios.items():
        existe = ruta.exists() and ruta.is_dir()
        estado[nombre] = existe
        if not existe:
            todos_existen = False

    return todos_existen, estado

def validar_archivos_codigo() -> Tuple[bool, Dict[str, bool]]:
    """Verifica que existan todos los archivos de código necesarios"""
    base_dir = Path(__file__).parent

    archivos = {
        'JiraOrange/configD.py': base_dir / 'JiraOrange' / 'configD.py',
        'JiraOrange/api/JiraAPIHandler.py': base_dir / 'JiraOrange' / 'api' / 'JiraAPIHandler.py',
        'JiraOrange/etl/extract.py': base_dir / 'JiraOrange' / 'etl' / 'extract.py',
        'JiraOrange/etl/transform.py': base_dir / 'JiraOrange' / 'etl' / 'transform.py',
        'JiraOrange/etl/parser.py': base_dir / 'JiraOrange' / 'etl' / 'parser.py',
        'JiraOrange/utils/utils.py': base_dir / 'JiraOrange' / 'utils' / 'utils.py',
        'JiraOrange/jira_bugs_to_json.py': base_dir / 'JiraOrange' / 'jira_bugs_to_json.py',
        'JiraOrange/jira_delivs_to_json.py': base_dir / 'JiraOrange' / 'jira_delivs_to_json.py',
        'JiraOrange/jira_bugs_etl.py': base_dir / 'JiraOrange' / 'jira_bugs_etl.py',
        'JiraOrange/jira_delivs_etl.py': base_dir / 'JiraOrange' / 'jira_delivs_etl.py',
    }

    estado = {}
    todos_existen = True

    for nombre, ruta in archivos.items():
        existe = ruta.exists() and ruta.is_file()
        estado[nombre] = existe
        if not existe:
            todos_existen = False

    return todos_existen, estado

def validar_variables_entorno() -> Tuple[bool, Dict[str, str]]:
    """Verifica que las variables de entorno estén configuradas"""
    from dotenv import load_dotenv

    # Cargar variables del .env
    base_dir = Path(__file__).parent
    env_file = base_dir / '.env'

    if not env_file.exists():
        return False, {'ERROR': 'Archivo .env no existe'}

    load_dotenv(env_file)

    variables = {}
    todas_ok = True

    # Verificar USUARIO
    usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
    if usuario:
        variables['USUARIO/JIRA_USER'] = f"Configurado ({usuario[:3]}***)"
    else:
        variables['USUARIO/JIRA_USER'] = "NO CONFIGURADO"
        todas_ok = False

    # Verificar PASS
    password = os.getenv('PASS') or os.getenv('PASSWORD') or os.getenv('JIRA_PASSWORD')
    if password:
        variables['PASS/PASSWORD'] = f"Configurado (***)"
    else:
        variables['PASS/PASSWORD'] = "NO CONFIGURADO"
        todas_ok = False

    return todas_ok, variables

def validar_archivos_entrada() -> Tuple[bool, Dict[str, str]]:
    """Verifica que existan archivos de entrada necesarios"""
    base_dir = Path(__file__).parent

    archivos = {
        'incidencias_in.csv': base_dir / 'in' / 'incidencias_in.csv',
    }

    estado = {}
    hay_archivos = False

    for nombre, ruta in archivos.items():
        if ruta.exists():
            # Verificar que no esté vacío
            size = ruta.stat().st_size
            if size > 0:
                estado[nombre] = f"Existe ({size} bytes)"
                hay_archivos = True
            else:
                estado[nombre] = "Existe pero está vacío"
        else:
            estado[nombre] = "NO EXISTE"

    return hay_archivos, estado

def validar_conexion_jira(verbose: bool = False) -> Tuple[bool, str]:
    """Verifica conectividad con Jira"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from JiraOrange.api import JiraAPIHandler

        jira = JiraAPIHandler.JiraAPIHandler()

        # Intentar una consulta simple
        response = jira.get_issues("TEST-1")  # Issue de prueba

        if response.status_code in [200, 404]:  # 404 es OK, significa que conectó
            return True, f"Conexión exitosa (Status: {response.status_code})"
        else:
            return False, f"Respuesta inesperada (Status: {response.status_code})"

    except ValueError as e:
        return False, f"Error de configuración: {str(e)}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

def validar_permisos_escritura() -> Tuple[bool, Dict[str, bool]]:
    """Verifica permisos de escritura en directorios clave"""
    base_dir = Path(__file__).parent

    directorios = {
        'out/': base_dir / 'out',
        'JSON/BUGS/': base_dir / 'JSON' / 'BUGS',
        'JSON/DELIVS/': base_dir / 'JSON' / 'DELIVS',
    }

    estado = {}
    todos_ok = True

    for nombre, ruta in directorios.items():
        if not ruta.exists():
            estado[nombre] = False
            todos_ok = False
            continue

        # Intentar crear archivo temporal
        test_file = ruta / '.test_write_permission'
        try:
            test_file.touch()
            test_file.unlink()
            estado[nombre] = True
        except Exception:
            estado[nombre] = False
            todos_ok = False

    return todos_ok, estado

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Valida el entorno del proyecto Informe Jira Python'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra información detallada'
    )
    parser.add_argument(
        '--skip-jira',
        action='store_true',
        help='Omite la prueba de conexión a Jira'
    )
    args = parser.parse_args()

    print(f"\n{Color.BOLD}Validación del Entorno - Informe Jira Python{Color.END}")
    print(f"{'=' * 60}\n")

    errores = []
    advertencias = []

    # 1. Versión de Python
    print_header("1. Versión de Python")
    ok, msg = validar_version_python()
    print_check("Versión de Python", ok, msg)
    if not ok:
        errores.append("Versión de Python incompatible")

    # 2. Librerías
    print_header("2. Librerías Requeridas")
    ok, instaladas, faltantes = validar_librerias()

    if ok:
        print_check("Todas las librerías instaladas", True, f"{len(instaladas)} librerias encontradas")
        if args.verbose:
            for lib in instaladas:
                print(f"  - {lib}")
    else:
        print_check("Librerias requeridas", False, f"Faltan {len(faltantes)} librerias")
        for lib in faltantes:
            print(f"  - {Color.RED}{lib}{Color.END}")
        errores.append("Librerías faltantes")
        print(f"\n  {Color.YELLOW}Solución:{Color.END} pip install -r requirements.txt")

    # 3. Variables de entorno
    print_header("3. Variables de Entorno")
    ok, variables = validar_variables_entorno()

    for nombre, valor in variables.items():
        es_error = "NO CONFIGURADO" in valor
        print_check(nombre, not es_error, valor)
        if es_error:
            errores.append(f"Variable {nombre} no configurada")

    if not ok:
        print(f"\n  {Color.YELLOW}Solución:{Color.END}")
        print(f"  1. Copia .env.example a .env")
        print(f"  2. Edita .env con tus credenciales de Jira")

    # 4. Estructura de directorios
    print_header("4. Estructura de Directorios")
    ok, directorios = validar_estructura_directorios()

    if ok:
        print_check("Estructura de directorios", True, f"{len(directorios)} directorios OK")
        if args.verbose:
            for nombre in directorios:
                print(f"  - {nombre}")
    else:
        faltantes_dirs = [n for n, e in directorios.items() if not e]
        print_check("Estructura de directorios", False, f"Faltan {len(faltantes_dirs)} directorios")
        for nombre in faltantes_dirs:
            print(f"  - {Color.RED}{nombre}{Color.END}")
        advertencias.append("Directorios faltantes (se crearán automáticamente)")

    # 5. Archivos de código
    print_header("5. Archivos de Código")
    ok, archivos = validar_archivos_codigo()

    if ok:
        print_check("Archivos de codigo", True, f"{len(archivos)} archivos encontrados")
    else:
        faltantes_arch = [n for n, e in archivos.items() if not e]
        print_check("Archivos de codigo", False, f"Faltan {len(faltantes_arch)} archivos")
        for nombre in faltantes_arch:
            print(f"  - {Color.RED}{nombre}{Color.END}")
        errores.append("Archivos de código faltantes")

    # 6. Permisos de escritura
    print_header("6. Permisos de Escritura")
    ok, permisos = validar_permisos_escritura()

    for nombre, puede_escribir in permisos.items():
        print_check(f"Escritura en {nombre}", puede_escribir)
        if not puede_escribir:
            errores.append(f"Sin permisos de escritura en {nombre}")

    # 7. Archivos de entrada
    print_header("7. Archivos de Entrada")
    ok, archivos_entrada = validar_archivos_entrada()

    for nombre, estado in archivos_entrada.items():
        existe = "NO EXISTE" not in estado
        es_warning = "vacío" in estado
        print_check(nombre, existe, estado, warning=es_warning)

        if not existe:
            advertencias.append(f"Archivo de entrada {nombre} no encontrado")
        elif es_warning:
            advertencias.append(f"Archivo {nombre} está vacío")

    # 8. Conexión a Jira (opcional)
    if not args.skip_jira:
        print_header("8. Conexión a Jira")
        ok, msg = validar_conexion_jira(args.verbose)
        print_check("Conectividad con Jira", ok, msg)

        if not ok:
            advertencias.append("No se pudo conectar a Jira")
            print(f"\n  {Color.YELLOW}Nota:{Color.END} Puedes omitir esta prueba con --skip-jira")
    else:
        print_header("8. Conexión a Jira")
        print_check("Conectividad con Jira", True, "Omitida (--skip-jira)", warning=True)

    # RESUMEN FINAL
    print_header("RESUMEN")

    total_errores = len(errores)
    total_advertencias = len(advertencias)

    if total_errores == 0 and total_advertencias == 0:
        print(f"{Color.GREEN}{Color.BOLD}[OK] ENTORNO VALIDO{Color.END}")
        print(f"{Color.GREEN}El proyecto esta listo para ejecutarse.{Color.END}\n")
        print(f"Puedes ejecutar:")
        print(f"  - python JiraOrange/jira_bugs_to_json.py")
        print(f"  - python JiraOrange/jira_delivs_to_json.py")
        print(f"  - python JiraOrange/jira_bugs_etl.py")
        print(f"  - python JiraOrange/jira_delivs_etl.py")
        return 0

    elif total_errores == 0:
        print(f"{Color.YELLOW}{Color.BOLD}[!] ADVERTENCIAS ({total_advertencias}){Color.END}")
        print(f"{Color.YELLOW}El proyecto puede ejecutarse, pero revisa las advertencias:{Color.END}\n")
        for i, adv in enumerate(advertencias, 1):
            print(f"  {i}. {adv}")
        print()
        return 0

    else:
        print(f"{Color.RED}{Color.BOLD}[X] ENTORNO NO VALIDO{Color.END}")
        print(f"{Color.RED}Se encontraron {total_errores} errores:{Color.END}\n")
        for i, err in enumerate(errores, 1):
            print(f"  {i}. {err}")

        if total_advertencias > 0:
            print(f"\n{Color.YELLOW}Y {total_advertencias} advertencias:{Color.END}\n")
            for i, adv in enumerate(advertencias, 1):
                print(f"  {i}. {adv}")

        print(f"\n{Color.YELLOW}Soluciones rápidas:{Color.END}")
        print(f"  1. Instalar dependencias: pip install -r requirements.txt")
        print(f"  2. Configurar .env: cp .env.example .env && nano .env")
        print(f"  3. Crear directorios: python -c 'import JiraOrange.configD'")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
