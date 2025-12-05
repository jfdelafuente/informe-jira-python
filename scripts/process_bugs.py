#!/usr/bin/env python
"""
Script de procesamiento ETL para bugs de Jira

Lee los archivos JSON de bugs almacenados en 'data/json/bugs/',
los transforma y genera un archivo CSV de salida con los campos:
    - Incidencias
    - Bugs
    - Status
    - Proyecto

Genera el fichero de salida 'data/output/salida_bugs.csv'
"""
import sys
import time
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pandas as pd
from jira_etl.config import Config
from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.utils.file_utils import load_to_csv, mostrar_bugs
from jira_etl.etl.extract import extract_bugs
from jira_etl.etl.transform import transform, Data_Quality, eliminar_duplicados
from jira_etl.etl.parser import parsear_bugs


def main():
    """Ejecuta el proceso ETL completo para bugs"""
    # Configurar logging
    setup_logging('process_bugs.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando proceso ETL de bugs")
    logger.info("="*60)

    start_time = time.time()

    try:
        # Fase de extracción
        logger.info("▶ Fase de EXTRACCIÓN iniciada")
        print("▶ Extrayendo datos de archivos JSON...")

        extracted_data = extract_bugs()

        if extracted_data.empty:
            logger.warning("No se encontraron datos para procesar")
            print("⚠ No se encontraron archivos JSON de bugs para procesar")
            print(f"  Verifica que existan archivos en: {Config.BUGS_JSON_DIR}")
            return 1

        logger.info(f"Extraídos {len(extracted_data)} registros")
        print(f"  Extraídos: {len(extracted_data)} registros")

        # Fase de transformación
        logger.info("▶ Fase de TRANSFORMACIÓN iniciada")
        print("▶ Transformando datos...")

        # Eliminar duplicados
        extracted_data = eliminar_duplicados(extracted_data)

        # Parsear bugs
        dict_metrics = {}
        transformed_data = pd.DataFrame(dict_metrics, columns=['Incidencias', 'Bugs', 'Status', 'PRJ'])

        for index, row in extracted_data.iterrows():
            dict_metrics['Incidencias'], dict_metrics['Bugs'], dict_metrics['Status'], dict_metrics['PRJ'] = parsear_bugs(row)
            new_salida = pd.DataFrame(dict_metrics, columns=['Incidencias', 'Bugs', 'Status', 'PRJ'])
            transformed_data = pd.concat([transformed_data, new_salida])

        # Validar calidad de datos
        Data_Quality(transformed_data)

        # Filtrar datos
        df_filtrado = transform(transformed_data)
        logger.info(f"Transformados {len(df_filtrado)} registros")
        print(f"  Transformados: {len(df_filtrado)} registros")

        # Fase de carga
        logger.info("▶ Fase de CARGA iniciada")
        print("▶ Guardando resultados...")

        output_file = Config.OUTPUT_BUGS_CSV
        load_to_csv(str(output_file), df_filtrado)

        logger.info(f"Archivo generado: {output_file}")

        # Mostrar resumen de bugs
        print("\n📋 Bugs procesados:")
        print("-" * 60)
        bugs_list = mostrar_bugs(df_filtrado)
        print(bugs_list)

        # Resumen final
        duration = time.time() - start_time

        logger.info("="*60)
        logger.info(f"Proceso ETL completado exitosamente")
        logger.info(f"Registros procesados: {len(df_filtrado)}")
        logger.info(f"Archivo de salida: {output_file}")
        logger.info(f"Duración: {duration:.2f} segundos")
        logger.info("="*60)

        print("\n" + "="*60)
        print("✓ Proceso ETL completado exitosamente")
        print(f"  Registros procesados: {len(df_filtrado)}")
        print(f"  Archivo generado: {output_file}")
        print(f"  Duración: {duration:.2f} segundos")
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
