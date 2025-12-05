#!/usr/bin/env python
"""
Script para extraer deliveries desde Jira y guardarlas en JSON

Consulta en Jira las deliveries asociadas a los bugs especificados
y genera un fichero JSON por cada delivery en el directorio 'data/json/deliveries/'.
"""
import sys
import json
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.config import Config
from jira_etl.api.client import JiraAPIHandler
from jira_etl.utils.file_utils import load_to_json
from jira_etl.utils.logger import setup_logging, get_logger


def main():
    """Ejecuta el proceso de extracción de deliveries desde Jira"""
    # Configurar logging
    setup_logging('extract_deliveries.log')
    logger = get_logger(__name__)

    logger.info("="*60)
    logger.info("Iniciando extracción de deliveries desde Jira")
    logger.info("="*60)

    ficheros_procesados = 0

    try:
        # Inicializar cliente de Jira
        try:
            jira = JiraAPIHandler()
            logger.info("Cliente de Jira inicializado correctamente")
        except ValueError as e:
            logger.error(f"Error de configuración: {e}")
            print(f"ERROR: {e}")
            print("Verifica que el archivo .env tenga USUARIO y PASS configurados")
            return 1

        # JQL para buscar deliveries asociadas a bugs
        # NOTA: Este JQL debería parametrizarse o generarse dinámicamente
        sJQL = '''type = Delivery AND "Bug/s" in (WCS-9489, INTEPS-14777, CRM4TE-22756, INTEPS-14788, MIDOSS-6575,
INTEPS-14844, KRATOS-13746, TMCSDS-715, MICRO-49163, INTEPS-14774,
INTEPS-14791, INTEPS-14846, ARCLMU-39101, INTEPS-14968, INTEPS-14794,
ARCLMU-39135, INTEPS-14877, FRONTCO-33732, INTEPS-14849, INTEPS-14865,
INTEPS-14790, WCS-9487, INTEPS-14847, INTEPS-14879, INTEPS-14862,
FRONTMC-18773, TEI-7939, FRONTCO-33908, FRONTMC-18775, FDCOSP-1083,
INTEPS-14913, MICRO-49228, INTEPS-15059, FRONTAT-2263, PAEOSP-20558,
PAEOSP-20552, TEDTED-8012, FCOM-25211, TEI-7951, FRONTRE-25415)'''

        logger.info("Ejecutando consulta JQL para deliveries...")
        print("Consultando deliveries en Jira...")

        response = jira.get_delivs(sJQL)

        if response.status_code == 200:
            try:
                issues = response.json()
                total_issues = len(issues.get("issues", []))
                logger.info(f"Encontradas {total_issues} deliveries")
                print(f"Encontradas {total_issues} deliveries\n")

                for issue in issues["issues"]:
                    nom_file = issue["key"] + "_delivs_news.json"
                    output_file = Config.DELIVS_JSON_DIR / nom_file
                    load_to_json(str(output_file), issue)

                    print(f"✓ Generando: {nom_file}")
                    logger.info(f"Generado: {nom_file}")
                    ficheros_procesados += 1

            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error procesando respuesta de Jira: {e}")
                print(f"ERROR procesando respuesta: {e}")
                return 1
        else:
            logger.error(f"Error en consulta a Jira: Status {response.status_code}")
            print(f"ERROR: La consulta a Jira falló con status {response.status_code}")
            return 1

        # Resumen final
        logger.info("="*60)
        logger.info(f"Proceso completado: {ficheros_procesados} archivos generados")
        logger.info("="*60)

        print("\n" + "="*60)
        print(f"✓ Proceso completado exitosamente")
        print(f"  Archivos generados: {ficheros_procesados}")
        print(f"  Ubicación: {Config.DELIVS_JSON_DIR}")
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
