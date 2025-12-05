#!/usr/bin/env python
"""
Script para ejecutar el pipeline ETL completo

Ejecuta en secuencia:
1. Extracción de bugs desde Jira
2. Extracción de deliveries desde Jira
3. Procesamiento de bugs (ETL)
4. Procesamiento de deliveries (ETL)
"""
import sys
import time
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from jira_etl.utils.logger import setup_logging, get_logger
from jira_etl.utils.output import OutputManager
from jira_etl.config import Config


def run_script(script_name: str, description: str, output: OutputManager) -> int:
    """
    Ejecuta un script y retorna su código de salida.

    Args:
        script_name: Nombre del script a ejecutar
        description: Descripción del paso
        output: OutputManager para mensajes consistentes

    Returns:
        Código de salida del script (0 = éxito, != 0 = error)
    """
    logger = get_logger(__name__)
    output.section(description)

    logger.info(f"Ejecutando: {script_name}")

    # Importar y ejecutar el script
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        logger.error(f"No se encontró el script: {script_name}")
        output.error(f"No se encontro {script_name}")
        return 1

    try:
        # Ejecutar el módulo
        import importlib.util
        spec = importlib.util.spec_from_file_location("module", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ejecutar main() del módulo
        if hasattr(module, 'main'):
            result = module.main()
            if result == 0:
                output.success(f"Paso completado: {script_name}")
            return result if result is not None else 0
        else:
            logger.error(f"{script_name} no tiene función main()")
            output.error(f"{script_name} no tiene funcion main()")
            return 1

    except Exception as e:
        logger.error(f"Error ejecutando {script_name}: {e}", exc_info=True)
        output.error(f"ERROR: {e}")
        return 1


def main():
    """Ejecuta el pipeline ETL completo"""
    # Inicializar output manager
    output = OutputManager(use_colors=True)

    # Configurar logging
    setup_logging('full_etl_pipeline.log')
    logger = get_logger(__name__)

    output.header("PIPELINE ETL COMPLETO - JIRA")

    logger.info("="*70)
    logger.info("Iniciando pipeline ETL completo")
    logger.info("="*70)

    start_time = time.time()

    # Definir los pasos del pipeline
    steps = [
        ("extract_bugs.py", "Paso 1/4: Extraccion de Bugs desde Jira"),
        ("extract_deliveries.py", "Paso 2/4: Extraccion de Deliveries desde Jira"),
        ("process_bugs.py", "Paso 3/4: Procesamiento ETL de Bugs"),
        ("process_deliveries.py", "Paso 4/4: Procesamiento ETL de Deliveries"),
    ]

    # Ejecutar cada paso
    for i, (script, description) in enumerate(steps, 1):
        result = run_script(script, description, output)

        if result != 0:
            logger.error(f"El paso {i} fallo: {script}")
            output.separator()
            output.error(f"Pipeline interrumpido en el paso {i}/{len(steps)}")
            output.separator()
            return 1

        logger.info(f"Paso {i}/{len(steps)} completado exitosamente")

    # Resumen final
    duration = time.time() - start_time

    logger.info("="*70)
    logger.info("Pipeline ETL completado exitosamente")
    logger.info(f"Duración total: {duration:.2f} segundos")
    logger.info("="*70)

    # Estadísticas del pipeline
    stats = {
        'processed': len(steps),
        'success': len(steps),
        'duration': duration,
        'location': str(Config.OUTPUT_DIR)
    }

    output.summary(stats, "RESUMEN FINAL - PIPELINE COMPLETO")

    output.info("")
    output.info("Archivos generados:")
    output.info(f"  - {Config.OUTPUT_BUGS_CSV.name}")
    output.info(f"  - {Config.OUTPUT_DELIVS_CSV.name}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
