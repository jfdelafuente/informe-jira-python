#!/usr/bin/env python
"""
Script de procesamiento ETL para deliveries de Jira

Lee los archivos JSON de deliveries almacenados en 'data/json/deliveries/',
los transforma y genera un archivo CSV de salida.

Genera el fichero de salida 'data/output/salida_delivs.csv'
"""
import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pandas as pd
from jira_etl.config import Config
from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.utils.file_utils import load_to_csv
from jira_etl.etl.extract import extract_delivs
from jira_etl.etl.parser import parsear_delivs
from jira_etl.etl.transform import Data_Quality


def main():
    """Ejecuta el proceso ETL completo para deliveries"""
    # Configurar logging
    setup_logging('process_deliveries.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando proceso ETL de deliveries")
    logger.info("="*60)

    try:
        # Fase de extracción
        logger.info("▶ Fase de EXTRACCIÓN iniciada")
        print("▶ Extrayendo datos de archivos JSON...")

        extracted_delivs = extract_delivs()

        if extracted_delivs.empty:
            logger.warning("No se encontraron datos para procesar")
            print("⚠ No se encontraron archivos JSON de deliveries para procesar")
            print(f"  Verifica que existan archivos en: {Config.DELIVS_JSON_DIR}")
            return 1

        logger.info(f"Extraídos {len(extracted_delivs)} registros")
        print(f"  Extraídos: {len(extracted_delivs)} registros")

        # Fase de transformación
        logger.info("▶ Fase de TRANSFORMACIÓN iniciada")
        print("▶ Transformando datos...")

        lista_delivs = []
        for index, row in extracted_delivs.iterrows():
            lista_delivs += parsear_delivs(row)

        transformed_data = pd.DataFrame(lista_delivs)
        logger.info(f"Transformados {len(transformed_data)} registros")
        print(f"  Transformados: {len(transformed_data)} registros")

        # Validar calidad de datos (opcional - comentado en original)
        # Data_Quality(transformed_data)

        # Fase de carga
        logger.info("▶ Fase de CARGA iniciada")
        print("▶ Guardando resultados...")

        output_file = Config.OUTPUT_DELIVS_CSV
        load_to_csv(str(output_file), transformed_data)

        logger.info(f"Archivo generado: {output_file}")

        # Resumen final
        logger.info("="*60)
        logger.info(f"Proceso ETL completado exitosamente")
        logger.info(f"Registros procesados: {len(transformed_data)}")
        logger.info(f"Archivo de salida: {output_file}")
        logger.info("="*60)

        print("\n" + "="*60)
        print("✓ Proceso ETL completado exitosamente")
        print(f"  Registros procesados: {len(transformed_data)}")
        print(f"  Archivo generado: {output_file}")
        print("="*60)

        return 0

    except Exception as e:
        logger.error(f"Error en el proceso ETL: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
