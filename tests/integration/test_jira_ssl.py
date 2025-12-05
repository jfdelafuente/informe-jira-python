"""
Script de prueba para verificar conectividad SSL con Jira
"""
import sys
import logging
from pathlib import Path

# Agregar src al path para importar el paquete jira_etl
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from jira_etl.api.client import JiraAPIHandler

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s'
)


def main():
    """Ejecuta pruebas de conectividad SSL con Jira"""
    print("=" * 60)
    print("PRUEBA DE CONEXION SSL A JIRA")
    print("=" * 60)

    try:
        print("\n1. Inicializando cliente Jira...")
        jira = JiraAPIHandler()
        print("   [OK] Cliente inicializado")

        print("\n2. Probando conexion con issue TEST-1...")
        response = jira.get_issues("TEST-1")
        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            print("   [OK] Conexion exitosa - Issue encontrado")
        elif response.status_code == 404:
            print("   [OK] Conexion exitosa - Issue no existe (pero conecto)")
        elif response.status_code == 401:
            print("   [ERROR] Error de autenticacion - Verifica credenciales")
        else:
            print(f"   [?] Status inesperado: {response.status_code}")

    except ValueError as e:
        print(f"\n[ERROR] Error de configuracion: {e}")
        print("\nVerifica tu archivo .env:")
        print("  - USUARIO=tu_usuario")
        print("  - PASSWORD=tu_password")
        print("  - JIRA_VERIFY_SSL=false")

    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        print("\nTraceback completo:")
        traceback.print_exc()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
