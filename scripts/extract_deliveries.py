#!/usr/bin/env python
"""
Script optimizado para extraer deliveries desde Jira y guardarlas en JSON

Consulta en Jira las deliveries asociadas a los bugs especificados
y genera un fichero JSON por cada delivery en el directorio 'data/json/deliveries/'.

Optimizaciones:
- Procesamiento paralelo de escrituras
- Mejor manejo de errores
- Progress feedback en tiempo real
- Carga dinámica de JQL desde archivo
"""
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import load_to_json
from jira_etl.utils.logger import setup_logging, get_logger


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
    # Configurar logging
    setup_logging('extract_deliveries.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando extracción OPTIMIZADA de deliveries desde Jira")
    logger.info("="*60)

    start_time = time.time()
    ficheros_procesados = 0
    ficheros_fallidos = 0

    try:
        print("="*60)
        print("[+] Extraccion de Deliveries desde Jira")
        print("[+] Modo: Procesamiento paralelo optimizado")
        print("="*60)

        # Inicializar cliente de Jira
        try:
            jira = JiraAPIHandler()
            logger.info("Cliente de Jira inicializado correctamente")
            print("[+] Cliente Jira inicializado")
        except ValueError as e:
            logger.error(f"Error de configuración: {e}")
            print(f"ERROR: {e}")
            print("Verifica que el archivo .env tenga USUARIO y PASS configurados")
            return 1

        # Cargar JQL
        sJQL = load_jql_from_file()
        logger.info(f"JQL cargado: {sJQL[:100]}...")

        logger.info("Ejecutando consulta JQL para deliveries...")
        print("\n[+] Consultando deliveries en Jira...")

        response = jira.get_delivs(sJQL)

        if response.status_code == 200:
            try:
                issues_data = response.json()
                issues = issues_data.get("issues", [])
                total_issues = len(issues)

                logger.info(f"Encontradas {total_issues} deliveries")
                print(f"[+] Encontradas {total_issues} deliveries")
                print(f"\n[+] Guardando archivos JSON en paralelo...")

                if total_issues == 0:
                    print("\n[!] No se encontraron deliveries con el JQL especificado")
                    logger.warning("No se encontraron deliveries")
                    return 0

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
                                status = "[OK]"
                                logger.info(f"Generado: {filename}")
                            else:
                                ficheros_fallidos += 1
                                status = "[ERROR]"
                                logger.error(f"Error generando {filename}: {message}")

                            # Progress feedback
                            progress = idx / total_issues * 100
                            print(f"  {status} [{idx}/{total_issues}] {filename} ({progress:.1f}%)")

                        except Exception as e:
                            ficheros_fallidos += 1
                            key = issue.get("key", "UNKNOWN")
                            logger.error(f"Error procesando {key}: {e}")
                            print(f"  [ERROR] [{idx}/{total_issues}] {key}: {str(e)}")

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error procesando respuesta de Jira: {e}")
                print(f"ERROR procesando respuesta: {e}")
                return 1
        else:
            logger.error(f"Error en consulta Jira: Status {response.status_code}")
            print(f"ERROR: Status {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return 1

        # Resumen final
        duration = time.time() - start_time
        throughput = total_issues / duration if duration > 0 else 0

        logger.info("="*60)
        logger.info(f"Proceso completado: {ficheros_procesados} archivos generados")
        logger.info(f"Exitosos: {ficheros_procesados}, Fallidos: {ficheros_fallidos}")
        logger.info(f"Duración: {duration:.2f} segundos ({throughput:.2f} delivs/seg)")
        logger.info("="*60)

        print("\n" + "="*60)
        print(f"[OK] Proceso completado exitosamente")
        print(f"  Deliveries procesadas: {total_issues}")
        print(f"  Archivos generados: {ficheros_procesados}")
        print(f"  Fallidos: {ficheros_fallidos}")
        print(f"  Duracion: {duration:.2f} segundos")
        print(f"  Rendimiento: {throughput:.2f} deliveries/segundo")
        print(f"  Ubicacion: {Config.DELIVS_JSON_DIR}")
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
