"""Configuración de pytest y fixtures compartidos"""
import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Retorna la raíz del proyecto"""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_data_dir(project_root):
    """Retorna el directorio de datos de ejemplo para tests"""
    return project_root / 'tests' / 'fixtures'
