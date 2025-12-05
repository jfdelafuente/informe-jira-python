#!/usr/bin/env python
"""
Script optimizado para extraer deliveries desde Jira y guardarlas en JSON

Consulta en Jira las deliveries asociadas a los bugs especificados
y genera un fichero JSON por cada delivery en el directorio 'data/json/deliveries/'.

Optimizaciones:
- Procesamiento paralelo de escrituras
- Sistema de output eficiente con colores
- Progress feedback en tiempo real
- Carga dinámica de JQL desde archivo
"""
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import load_to_json
from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.utils.output import OutputManager


def save_delivery(issue: Dict[str, Any], output_dir: Path) -> tuple:
    """
    Guarda una delivery en un archivo JSON.

    Args:
        issue: Datos de la delivery
        output_dir: Directorio de salida

    Returns:
        Tupla (success, filename, message)
    """
    try:
        nom_file = issue["key"] + "_delivs_news.json"
        output_file = output_dir / nom_file
        load_to_json(str(output_file), issue)
        return (True, nom_file, "OK")
    except Exception as e:
        key = issue.get("key", "UNKNOWN")
        return (False, key, f"ERROR: {str(e)}")


def load_jql_from_file() -> str:
    """
    Intenta cargar el JQL desde un archivo de configuración.
    Si no existe, usa el JQL por defecto.

    Returns:
        String con la consulta JQL
    """
    jql_file = Config.CONFIG_DIR / 'deliveries_jql.txt'

    if jql_file.exists():
        with open(jql_file, 'r', encoding='utf-8') as f:
            return f.read().strip()

    # JQL por defecto
    return '''type = Delivery AND "Bug/s" in (WCS-9489, INTEPS-14777, CRM4TE-22756, INTEPS-14788, MIDOSS-6575,
INTEPS-14844, KRATOS-13746, TMCSDS-715, MICRO-49163, INTEPS-14774,
INTEPS-14791, INTEPS-14846, ARCLMU-39101, INTEPS-14968, INTEPS-14794,
ARCLMU-39135, INTEPS-14877, FRONTCO-33732, INTEPS-14849, INTEPS-14865,
INTEPS-14790, WCS-9487, INTEPS-14847, INTEPS-14879, INTEPS-14862,
FRONTMC-18773, TEI-7939, FRONTCO-33908, FRONTMC-18775, FDCOSP-1083,
INTEPS-14913, MICRO-49228, INTEPS-15059, FRONTAT-2263, PAEOSP-20558,
PAEOSP-20552, TEDTED-8012, FCOM-25211, TEI-7951, FRONTRE-25415)'''


def main():
    """Ejecuta el proceso de extracción de deliveries desde Jira (optimizado)"""
    # Inicializar output manager
    output = OutputManager(use_colors=True)

    # Configurar logging
    setup_logging('extract_deliveries.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando extracción OPTIMIZADA de deliveries desde Jira")
    logger.info("="*60)

    output.header("EXTRACCION DE DELIVERIES DESDE JIRA")

    start_time = time.time()
    ficheros_procesados = 0
    ficheros_fallidos = 0

    try:
        output.section("Configuracion")
        output.info("  Modo: Procesamiento paralelo (max 10 workers)")

        # Inicializar cliente de Jira
        try:
            jira = JiraAPIHandler()
            logger.info("Cliente de Jira inicializado correctamente")
            output.success("Cliente Jira inicializado")
        except ValueError as e:
            logger.error(f"Error de configuración: {e}")
            output.error(str(e))
            output.info("Verifica que el archivo .env tenga USUARIO y PASS configurados")
            return 1

        # Cargar JQL
        sJQL = load_jql_from_file()
        logger.info(f"JQL cargado: {sJQL[:100]}...")

        logger.info("Ejecutando consulta JQL para deliveries...")
        output.section("Consultando deliveries en Jira")

        response = jira.get_delivs(sJQL)

        if response.status_code == 200:
            try:
                issues_data = response.json()
                issues = issues_data.get("issues", [])
                total_issues = len(issues)

                logger.info(f"Encontradas {total_issues} deliveries")
                output.success(f"Encontradas {total_issues} deliveries")

                if total_issues == 0:
                    output.warning("No se encontraron deliveries con el JQL especificado")
                    logger.warning("No se encontraron deliveries")
                    return 0

                output.section(f"Guardando {total_issues} archivos JSON en paralelo")

                # Procesar deliveries en paralelo
                with ThreadPoolExecutor(max_workers=min(10, total_issues)) as executor:
                    futures = {
                        executor.submit(save_delivery, issue, Config.DELIVS_JSON_DIR): issue
                        for issue in issues
                    }

                    for idx, future in enumerate(as_completed(futures), 1):
                        issue = futures[future]
                        try:
                            success, filename, message = future.result()

                            if success:
                                ficheros_procesados += 1
                                status = "OK"
                                logger.info(f"Generado: {filename}")
                            else:
                                ficheros_fallidos += 1
                                status = "ERROR"
                                logger.error(f"Error generando {filename}: {message}")

                            # Progress feedback
                            output.progress(idx, total_issues, filename, 0, status)

                        except Exception as e:
                            ficheros_fallidos += 1
                            key = issue.get("key", "UNKNOWN")
                            logger.error(f"Error procesando {key}: {e}")
                            output.error(f"[{idx}/{total_issues}] {key}: {str(e)}")

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error procesando respuesta de Jira: {e}")
                output.error(f"Error procesando respuesta: {e}")
                return 1
        else:
            logger.error(f"Error en consulta Jira: Status {response.status_code}")
            output.error(f"Status {response.status_code}")
            output.info(f"Respuesta: {response.text[:200]}")
            return 1

        # Preparar estadísticas
        duration = time.time() - start_time
        stats = {
            'processed': total_issues,
            'success': ficheros_procesados,
            'failed': ficheros_fallidos,
            'duration': duration,
            'location': str(Config.DELIVS_JSON_DIR)
        }

        # Logging final
        logger.info("="*60)
        logger.info(f"Proceso completado: {ficheros_procesados} archivos generados")
        logger.info(f"Exitosos: {ficheros_procesados}, Fallidos: {ficheros_fallidos}")
        logger.info(f"Duración: {duration:.2f} segundos")
        logger.info("="*60)

        # Mostrar resumen
        output.summary(stats, "RESUMEN FINAL - DELIVERIES")

        return 0

    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        output.error(f"ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
