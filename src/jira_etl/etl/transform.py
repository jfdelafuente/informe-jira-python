"""Funciones de transformación de datos"""
import pandas as pd
from ..utils.logger import get_logger

logger = get_logger(__name__)


def transform(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos filtrando registros cancelados.

    Args:
        data: DataFrame con los datos originales

    Returns:
        DataFrame filtrado
    """
    logger.info(f"Transformando {len(data)} registros")
    df_filtrado = data[data["Status"] != "Cancelled / Won't Do"]
    logger.info(f"Filtrados {len(data) - len(df_filtrado)} registros cancelados")
    return df_filtrado


def Data_Quality(load_df: pd.DataFrame) -> bool:
    """
    Valida la calidad de los datos antes de cargar.

    Args:
        load_df: DataFrame a validar

    Returns:
        True si los datos son válidos, False en caso contrario

    Raises:
        Exception: Si se encuentran valores nulos
    """
    # Checking Whether the DataFrame is empty
    if load_df.empty:
        logger.warning('No se extrajeron datos')
        return False

    # Checking for Nulls in our data frame
    if load_df.isnull().values.any():
        logger.error("Se encontraron valores nulos en los datos")
        raise Exception("Null values found")

    logger.info("Validación de calidad de datos exitosa")
    return True


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas duplicadas del DataFrame.

    Args:
        df: DataFrame con posibles duplicados

    Returns:
        DataFrame sin duplicados
    """
    original_count = len(df)
    df_sin_duplicados = df.drop_duplicates()
    duplicados = original_count - len(df_sin_duplicados)

    if duplicados > 0:
        logger.info(f"Eliminados {duplicados} registros duplicados")

    return df_sin_duplicados
