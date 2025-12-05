"""Módulo ETL (Extract, Transform, Load)"""
from .extract import extract_bugs, extract_delivs
from .transform import transform, eliminar_duplicados, Data_Quality
from .parser import parsear_bugs, parsear_delivs

__all__ = [
    'extract_bugs',
    'extract_delivs',
    'transform',
    'eliminar_duplicados',
    'Data_Quality',
    'parsear_bugs',
    'parsear_delivs'
]
