#!/usr/bin/env python
"""
Script optimizado para extraer bugs desde Jira y guardarlos en JSON

Consulta en Jira los bugs asociados a las incidencias EPSILON incluidas
en el fichero 'incidencias_in.csv' y genera un fichero JSON en el
directorio 'data/json/bugs/' por cada incidencia.

Optimizaciones:
- Procesamiento por lotes para reducir llamadas HTTP
- Procesamiento paralelo con ThreadPoolExecutor
- Sistema de output eficiente con colores
- Progress feedback en tiempo real
"""
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple, Dict, Any
from threading import Lock

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import extract_from_csv, load_to_json
from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.utils.output import OutputManager
from jira_etl.etl.transform import Data_Quality


def process_single_incidencia(
    jira: JiraAPIHandler,
    incidencia: str,
    index: int,
    total: int
) -> Tuple[bool, str, int, str]:
    """
    Procesa una incidencia individual.

    Args:
        jira: Cliente de Jira
        incidencia: Número de incidencia
        index: Índice actual (0-based)
        total: Total de incidencias

    Returns:
        Tupla (success, incidencia, bugs_count, message)
    """
    try:
        estatus, texto = jira.get_bug_to_json(incidencia)

        if estatus == 200 and texto:
            nom_fichero = f"{incidencia}_bugs_new.json"
            output_file = Config.BUGS_JSON_DIR / nom_fichero
            load_to_json(str(output_file), texto)

            total_bugs = texto.get('total', 0)
            return (True, incidencia, total_bugs, f"OK -> {nom_fichero}")
        else:
            return (False, incidencia, 0, f"SKIP - Status {estatus}")

    except Exception as e:
        return (False, incidencia, 0, f"ERROR - {str(e)}")


def process_batch(
    jira: JiraAPIHandler,
    incidencias: list,
    output: OutputManager,
    batch_size: int = 10
) -> Dict[str, Any]:
    """
    Procesa incidencias en lotes para optimizar.

    Args:
        jira: Cliente de Jira
        incidencias: Lista de incidencias a procesar
        output: Gestor de salida
        batch_size: Tamaño del lote

    Returns:
        Diccionario con resultados del procesamiento
    """
    logger = get_logger(__name__)
    results = {
        'processed': 0,
        'success': 0,
        'failed': 0,
        'total_bugs': 0
    }

    total = len(incidencias)

    # Procesar en lotes
    for i in range(0, total, batch_size):
        batch = incidencias[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        output.section(f"Procesando lote {batch_num}/{total_batches} ({len(batch)} incidencias)")

        # Procesar lote en paralelo
        with ThreadPoolExecutor(max_workers=min(5, len(batch))) as executor:
            futures = {
                executor.submit(
                    process_single_incidencia,
                    jira,
                    inc,
                    idx,
                    total
                ): (inc, idx) for idx, inc in enumerate(batch, start=i)
            }

            for future in as_completed(futures):
                inc, idx = futures[future]
                try:
                    success, incidencia, bugs_count, message = future.result()
                    results['processed'] += 1

                    if success:
                        results['success'] += 1
                        results['total_bugs'] += bugs_count
                        status = "OK"
                        logger.info(f"OK {incidencia} - Bugs: {bugs_count}")
                    else:
                        results['failed'] += 1
                        status = "SKIP" if "SKIP" in message else "ERROR"
                        logger.warning(f"{status} {incidencia} - {message}")

                    # Progress feedback
                    output.progress(idx + 1, total, incidencia, bugs_count, status)

                except Exception as e:
                    logger.error(f"Error en future para {inc}: {e}")
                    results['processed'] += 1
                    results['failed'] += 1
                    output.error(f"[{idx + 1}/{total}] {inc}: {str(e)}")

    return results


def main():
    """Ejecuta el proceso de extracción de bugs desde Jira (optimizado)"""
    # Inicializar output manager
    output = OutputManager(use_colors=True)

    # Configurar logging
    setup_logging('extract_bugs.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando extracción OPTIMIZADA de bugs desde Jira")
    logger.info("="*60)

    output.header("EXTRACCION DE BUGS DESDE JIRA")

    if not HAS_COLORS:
        output.info("Nota: Instala 'colorama' para ver con colores (pip install colorama)")

    start_time = time.time()
    archivo_entrada = Config.INPUT_FILE

    try:
        # Validar que existe el archivo de entrada
        if not archivo_entrada.exists():
            logger.error(f"No se encontró el archivo de entrada: {archivo_entrada}")
            output.error(f"No se encontro el archivo {archivo_entrada}")
            output.info(f"Por favor, crea el archivo con las incidencias a procesar.")
            return 1

        # Leer incidencias desde CSV
        logger.info(f"Leyendo incidencias desde: {archivo_entrada}")
        df_epsilons = extract_from_csv(str(archivo_entrada))

        output.section(f"Configuracion")
        output.info(f"  Archivo entrada: {archivo_entrada.name}")
        output.info(f"  Incidencias: {len(df_epsilons)}")
        output.info(f"  Modo: Procesamiento paralelo (max 5 workers)")
        output.info(f"  Batch size: 10")

        # Validar calidad de datos
        if not Data_Quality(df_epsilons):
            logger.error("Error en la validación de calidad de datos")
            output.error("No se pudo validar la calidad de los datos")
            return 1

        logger.info("Validación de calidad de datos: OK")

        # Inicializar cliente de Jira
        try:
            jira = JiraAPIHandler()
            logger.info("Cliente de Jira inicializado correctamente")
            output.success("Cliente Jira inicializado")
        except ValueError as e:
            logger.error(f"Error de configuración de Jira: {e}")
            output.error(str(e))
            output.info("Verifica que el archivo .env tenga USUARIO y PASS configurados")
            return 1

        # Extraer lista de incidencias
        incidencias = df_epsilons['Incidencia'].tolist()

        # Procesar por lotes (optimizado)
        results = process_batch(jira, incidencias, output, batch_size=10)

        # Calcular estadísticas
        duration = time.time() - start_time
        results['duration'] = duration
        results['location'] = str(Config.BUGS_JSON_DIR)

        # Logging final
        logger.info("="*60)
        logger.info(f"Proceso completado: {results['success']} archivos generados")
        logger.info(f"Exitosos: {results['success']}, Fallidos: {results['failed']}")
        logger.info(f"Total bugs encontrados: {results['total_bugs']}")
        logger.info(f"Duración: {duration:.2f} segundos")
        logger.info("="*60)

        # Mostrar resumen
        output.summary(results, "RESUMEN FINAL - BUGS")

        return 0

    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        output.error(f"ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
