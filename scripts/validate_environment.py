#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de validacion actualizado para la nueva estructura"""
import sys
import os
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

print("[OK] Script de validacion - Nueva Estructura")
print("=" * 60)

# Validar Python
print("\n[+] Validando Python...")
version = sys.version_info
print(f"   Python {version.major}.{version.minor}.{version.micro}")

# Validar estructura
print("\n[+] Validando estructura de directorios...")
base_dir = Path(__file__).parent.parent

dirs_nuevos = [
    'src/jira_etl',
    'scripts',
    'data/input',
    'data/output',
    'data/json/bugs',
    'data/json/deliveries',
]

for d in dirs_nuevos:
    path = base_dir / d
    exists = path.exists()
    symbol = "[OK]" if exists else "[NO]"
    print(f"   {symbol} {d}")

# Validar archivos clave
print("\n[+] Validando archivos clave...")
files = [
    'src/jira_etl/config.py',
    'scripts/extract_bugs.py',
    'scripts/run_full_etl.py',
    'pyproject.toml',
    'Makefile',
]

for f in files:
    path = base_dir / f
    exists = path.exists()
    symbol = "[OK]" if exists else "[NO]"
    print(f"   {symbol} {f}")

# Validar variables de entorno
print("\n[+] Validando variables de entorno...")
from dotenv import load_dotenv
load_dotenv()

usuario = os.getenv('USUARIO') or os.getenv('JIRA_USER')
password = os.getenv('PASS') or os.getenv('PASSWORD')

if usuario and password:
    print(f"   [OK] Credenciales configuradas")
else:
    print(f"   [NO] Faltan credenciales en .env")

print("\n" + "=" * 60)
print("[OK] Validacion completada")
print("\nPara ejecutar el proyecto:")
print("  make run-etl")
print("  python scripts/run_full_etl.py")
