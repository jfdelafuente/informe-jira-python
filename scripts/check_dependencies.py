#!/usr/bin/env python
"""
Script para verificar que todas las dependencias están instaladas correctamente

Este script verifica:
1. Versión de Python
2. Dependencias principales instaladas
3. Versiones compatibles
4. Importación correcta de módulos

Uso:
    python scripts/check_dependencies.py

    # O con make
    make check-deps

    # O con run.ps1 (Windows)
    .\run.ps1 check-deps
"""
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from jira_etl.utils.output import OutputManager
    HAS_OUTPUT_MANAGER = True
except ImportError:
    HAS_OUTPUT_MANAGER = False


def print_colored(message: str, color: str = ""):
    """Imprime mensaje con color si OutputManager está disponible"""
    if HAS_OUTPUT_MANAGER:
        output = OutputManager(use_colors=True)
        if color == "success":
            output.success(message)
        elif color == "error":
            output.error(message)
        elif color == "warning":
            output.warning(message)
        elif color == "info":
            output.info(message)
        else:
            print(message)
    else:
        print(message)


def check_python_version():
    """Verifica la versión de Python"""
    print_colored("\n=== Verificando Version de Python ===", "info")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print(f"  Version instalada: Python {version_str}")

    if version.major == 3 and version.minor >= 8:
        print_colored("  Python version OK (>= 3.8)", "success")
        return True
    else:
        print_colored(f"  ERROR: Se requiere Python >= 3.8", "error")
        print_colored(f"  Version actual: {version_str}", "error")
        return False


def check_dependency(package_name: str, import_name: str = None, min_version: str = None):
    """
    Verifica una dependencia individual

    Args:
        package_name: Nombre del paquete en pip
        import_name: Nombre para importar (si es diferente a package_name)
        min_version: Versión mínima requerida (opcional)

    Returns:
        bool: True si la dependencia está OK
    """
    if import_name is None:
        import_name = package_name.replace('-', '_')

    try:
        # Intentar importar el módulo
        module = __import__(import_name)

        # Obtener versión
        version = None
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'VERSION'):
            version = module.VERSION
        elif hasattr(module, 'version'):
            version = module.version

        # Mostrar resultado
        version_str = f" (v{version})" if version else ""
        print(f"  [OK] {package_name}{version_str}")

        # Verificar versión mínima si se especificó
        if min_version and version:
            from packaging import version as pkg_version
            if pkg_version.parse(version) < pkg_version.parse(min_version):
                print_colored(f"      ADVERTENCIA: Version {version} < {min_version} (minima)", "warning")
                return False

        return True

    except ImportError:
        print_colored(f"  [FALTA] {package_name} - NO INSTALADO", "error")
        return False
    except Exception as e:
        print_colored(f"  [ERROR] {package_name} - Error al verificar: {e}", "error")
        return False


def check_all_dependencies():
    """Verifica todas las dependencias del proyecto"""
    print_colored("\n=== Verificando Dependencias Principales ===", "info")

    dependencies = [
        # (package_name, import_name, min_version)
        ('requests', 'requests', '2.28.0'),
        ('pandas', 'pandas', '1.5.0'),
        ('python-dotenv', 'dotenv', '0.20.0'),
        ('colorama', 'colorama', '0.4.6'),
        ('openpyxl', 'openpyxl', '3.0.0'),
    ]

    results = []
    for dep in dependencies:
        if len(dep) == 3:
            package, import_name, min_ver = dep
            result = check_dependency(package, import_name, min_ver)
        else:
            package, import_name = dep
            result = check_dependency(package, import_name)
        results.append(result)

    return all(results)


def check_project_imports():
    """Verifica que los módulos del proyecto se pueden importar"""
    print_colored("\n=== Verificando Modulos del Proyecto ===", "info")

    modules = [
        ('jira_etl.config', 'Config'),
        ('jira_etl.api.client', 'JiraAPIHandler'),
        ('jira_etl.utils.logger', 'setup_logging'),
        ('jira_etl.utils.output', 'OutputManager'),
        ('jira_etl.etl.extract', 'extract_bugs'),
        ('jira_etl.etl.transform', 'transform'),
        ('jira_etl.etl.parser', 'parsear_bugs'),
    ]

    results = []
    for module_path, item_name in modules:
        try:
            module = __import__(module_path, fromlist=[item_name])
            if hasattr(module, item_name):
                print(f"  [OK] {module_path}.{item_name}")
                results.append(True)
            else:
                print_colored(f"  [ERROR] {module_path} no tiene '{item_name}'", "error")
                results.append(False)
        except ImportError as e:
            print_colored(f"  [ERROR] No se puede importar {module_path}: {e}", "error")
            results.append(False)
        except Exception as e:
            print_colored(f"  [ERROR] Error verificando {module_path}: {e}", "error")
            results.append(False)

    return all(results)


def show_recommendations():
    """Muestra recomendaciones según el sistema operativo"""
    print_colored("\n=== Recomendaciones ===", "info")

    import platform
    system = platform.system()

    if system == "Windows":
        print("\n  Si tienes problemas con pandas:")
        print("    pip install -r requirements-compatible.txt")
        print("\n  Para desarrollo:")
        print("    pip install -r requirements-dev.txt")
    else:
        print("\n  Para instalar todas las dependencias:")
        print("    pip install -r requirements.txt")
        print("\n  Para desarrollo:")
        print("    pip install -r requirements-dev.txt")

    print("\n  Para mas informacion:")
    print("    Consulta REQUIREMENTS.md")


def main():
    """Función principal"""
    print_colored("\n" + "="*60)
    print_colored("  VERIFICACION DE DEPENDENCIAS - JIRA ETL")
    print_colored("="*60)

    # Verificar Python
    python_ok = check_python_version()

    # Verificar dependencias
    deps_ok = check_all_dependencies()

    # Verificar imports del proyecto
    imports_ok = check_project_imports()

    # Resumen
    print_colored("\n" + "="*60, "info")
    print_colored("  RESUMEN DE VERIFICACION", "info")
    print_colored("="*60, "info")

    print(f"\n  Python version:        {'OK' if python_ok else 'FALLO'}")
    print(f"  Dependencias:          {'OK' if deps_ok else 'FALLO'}")
    print(f"  Modulos del proyecto:  {'OK' if imports_ok else 'FALLO'}")

    all_ok = python_ok and deps_ok and imports_ok

    if all_ok:
        print_colored("\n  TODAS LAS VERIFICACIONES PASARON", "success")
        print_colored("  El proyecto esta listo para ejecutarse", "success")
        show_recommendations()
        return 0
    else:
        print_colored("\n  ALGUNAS VERIFICACIONES FALLARON", "error")
        print_colored("  Por favor, instala las dependencias faltantes", "error")
        show_recommendations()
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerificacion cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
