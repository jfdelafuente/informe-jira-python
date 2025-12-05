#!/usr/bin/env python
"""
Script para extraer bugs desde Jira y guardarlos en JSON

Consulta en Jira los bugs asociados a las incidencias EPSILON incluidas
en el fichero 'incidencias_in.csv' y genera un fichero JSON en el
directorio 'data/json/bugs/' por cada incidencia.
"""
import sys
import time
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import extract_from_csv, load_to_json
from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.etl.transform import Data_Quality


def main():
    """Ejecuta el proceso de extracción de bugs desde Jira"""
    # Configurar logging
    setup_logging('extract_bugs.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando extracción de bugs desde Jira")
    logger.info("="*60)

    start_time = time.time()
    ficheros_procesados = 0
    archivo_entrada = Config.INPUT_FILE

    try:
        # Validar que existe el archivo de entrada
        if not archivo_entrada.exists():
            logger.error(f"No se encontró el archivo de entrada: {archivo_entrada}")
            print(f"ERROR: No se encontró el archivo {archivo_entrada}")
            print(f"Por favor, crea el archivo con las incidencias a procesar.")
            return 1

        # Leer incidencias desde CSV
        logger.info(f"Leyendo incidencias desde: {archivo_entrada}")
        df_epsilons = extract_from_csv(str(archivo_entrada))
        print(f"Leídas {len(df_epsilons)} incidencias desde {archivo_entrada.name}")

        # Validar calidad de datos
        if not Data_Quality(df_epsilons):
            logger.error("Error en la validación de calidad de datos")
            print("ERROR: No se pudo validar la calidad de los datos")
            return 1

        logger.info("Validación de calidad de datos: OK")

        # Inicializar cliente de Jira
        try:
            jira = JiraAPIHandler()
            logger.info("Cliente de Jira inicializado correctamente")
        except ValueError as e:
            logger.error(f"Error de configuración de Jira: {e}")
            print(f"ERROR: {e}")
            print("Verifica que el archivo .env tenga USUARIO y PASS configurados")
            return 1

        # Procesar cada incidencia
        for index, row in df_epsilons.iterrows():
            row_inc = row['Incidencia']

            try:
                logger.info(f"Procesando incidencia {index + 1}/{len(df_epsilons)}: {row_inc}")
                estatus, texto = jira.get_bug_to_json(row_inc)

                if estatus == 200 and texto:
                    nom_fichero = f"{row_inc}_bugs_new.json"
                    output_file = Config.BUGS_JSON_DIR / nom_fichero
                    load_to_json(str(output_file), texto)

                    total_bugs = texto.get('total', 0)
                    logger.info(f"OK {row_inc} - Status: {estatus} - Bugs encontrados: {total_bugs}")
                    print(f"[OK] [{index + 1}/{len(df_epsilons)}] {row_inc}: {total_bugs} bugs -> {nom_fichero}")
                    ficheros_procesados += 1
                else:
                    logger.warning(f"SKIP {row_inc} - Status: {estatus} - Sin datos")
                    print(f"[SKIP] [{index + 1}/{len(df_epsilons)}] {row_inc}: No se encontraron bugs")

            except Exception as e:
                logger.error(f"Error procesando {row_inc}: {e}", exc_info=True)
                print(f"[ERROR] [{index + 1}/{len(df_epsilons)}] {row_inc}: ERROR - {e}")
                continue

        # Resumen final
        duration = time.time() - start_time
        logger.info("="*60)
        logger.info(f"Proceso completado: {ficheros_procesados} archivos generados")
        logger.info(f"Duración: {duration:.2f} segundos")
        logger.info("="*60)

        print("\n" + "="*60)
        print(f"[OK] Proceso completado exitosamente")
        print(f"  Archivos generados: {ficheros_procesados}/{len(df_epsilons)}")
        print(f"  Duracion: {duration:.2f} segundos")
        print(f"  Ubicacion: {Config.BUGS_JSON_DIR}")
        print("="*60)

        return 0

    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        print(f"\nERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
