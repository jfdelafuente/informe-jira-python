"""
Script para probar autenticación con Jira
Prueba diferentes endpoints para diagnosticar el problema
"""
import sys
import logging
from pathlib import Path

# Agregar src al path para importar el paquete jira_etl
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from jira_etl.api.client import JiraAPIHandler
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Silenciar logs de debug
logging.basicConfig(level=logging.WARNING)

# Cargar variables de entorno
load_dotenv()

def main():
    """Ejecuta pruebas de autenticación con Jira"""
    print("=" * 70)
    print("DIAGNOSTICO DE AUTENTICACION JIRA")
    print("=" * 70)

    usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
    password = os.getenv('PASS') or os.getenv('PASSWORD') or os.getenv('JIRA_PASSWORD')

    print(f"\nCredenciales detectadas:")
    print(f"  Usuario: {usuario}")
    print(f"  Password: {'*' * len(password) if password else 'NO CONFIGURADO'}")

    # Prueba 1: Endpoint de sesión
    print("\n" + "-" * 70)
    print("PRUEBA 1: Endpoint /rest/auth/1/session (verificar autenticacion)")
    print("-" * 70)

    try:
        url = "https://jira.si.orange.es/rest/auth/1/session"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(usuario, password),
            verify=False,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("[OK] Autenticacion valida")
            print(f"Usuario autenticado: {response.json().get('name', 'Unknown')}")
        else:
            print(f"[ERROR] {response.text[:200]}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Prueba 2: Endpoint de usuario
    print("\n" + "-" * 70)
    print("PRUEBA 2: Endpoint /rest/api/2/myself (info del usuario)")
    print("-" * 70)

    try:
        url = "https://jira.si.orange.es/rest/api/2/myself"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(usuario, password),
            verify=False,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Usuario: {data.get('displayName', 'Unknown')}")
            print(f"     Email: {data.get('emailAddress', 'Unknown')}")
        else:
            print(f"[ERROR] {response.text[:200]}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Prueba 3: Búsqueda JQL
    print("\n" + "-" * 70)
    print("PRUEBA 3: Busqueda JQL simple (permisos de lectura)")
    print("-" * 70)

    try:
        url = "https://jira.si.orange.es/rest/api/latest/search"
        params = {
            'jql': 'project is not EMPTY',
            'maxResults': 1
        }
        response = requests.get(
            url,
            auth=HTTPBasicAuth(usuario, password),
            params=params,
            verify=False,
            timeout=30
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            print(f"[OK] Puede buscar issues. Total encontrados: {total}")
            if data.get('issues'):
                first = data['issues'][0]
                print(f"     Ejemplo: {first.get('key')} - {first['fields'].get('summary', '')[:50]}")
        else:
            print(f"[ERROR] {response.text[:200]}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Diagnóstico final
    print("\n" + "-" * 70)
    print("DIAGNOSTICO")
    print("-" * 70)

    if response.status_code == 401:
        print("\n[ERROR] Credenciales incorrectas")
        print("\nSoluciones:")
        print("  1. Verifica USUARIO y PASS en .env")
        print("  2. Prueba acceder a https://jira.si.orange.es con esas credenciales")
    elif response.status_code == 403:
        print("\n[WARNING] Usuario autenticado pero sin permisos")
        print("\nPosibles causas:")
        print("  1. El usuario no tiene permisos de lectura en Jira")
        print("  2. La autenticacion basica HTTP esta deshabilitada")
        print("  3. Se requiere autenticacion OAuth/SSO")
        print("\nContacta al administrador de Jira")
    elif response.status_code == 200:
        print("\n[OK] Autenticacion y permisos correctos")
    else:
        print(f"\n[?] Status inesperado: {response.status_code}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
