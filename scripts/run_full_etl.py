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


def run_script(script_name: str, description: str) -> int:
    """
    Ejecuta un script y retorna su código de salida.

    Args:
        script_name: Nombre del script a ejecutar
        description: Descripción del paso

    Returns:
        Código de salida del script (0 = éxito, != 0 = error)
    """
    logger = get_logger(__name__)
    print("\n" + "="*70)
    print(f"🔄 {description}")
    print("="*70)

    logger.info(f"Ejecutando: {script_name}")

    # Importar y ejecutar el script
    script_path = Path(__file__).parent / script_name
    if not script_path.exists():
        logger.error(f"No se encontró el script: {script_name}")
        print(f"❌ ERROR: No se encontró {script_name}")
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
            return result if result is not None else 0
        else:
            logger.error(f"{script_name} no tiene función main()")
            return 1

    except Exception as e:
        logger.error(f"Error ejecutando {script_name}: {e}", exc_info=True)
        print(f"❌ ERROR: {e}")
        return 1


def main():
    """Ejecuta el pipeline ETL completo"""
    # Configurar logging
    setup_logging('full_etl_pipeline.log')
    logger = get_logger(__name__)

    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "PIPELINE ETL COMPLETO - JIRA" + " "*25 + "║")
    print("╚" + "═"*68 + "╝")

    logger.info("="*70)
    logger.info("Iniciando pipeline ETL completo")
    logger.info("="*70)

    start_time = time.time()

    # Definir los pasos del pipeline
    steps = [
        ("extract_bugs.py", "Paso 1/4: Extracción de Bugs desde Jira"),
        ("extract_deliveries.py", "Paso 2/4: Extracción de Deliveries desde Jira"),
        ("process_bugs.py", "Paso 3/4: Procesamiento ETL de Bugs"),
        ("process_deliveries.py", "Paso 4/4: Procesamiento ETL de Deliveries"),
    ]

    # Ejecutar cada paso
    for i, (script, description) in enumerate(steps, 1):
        result = run_script(script, description)

        if result != 0:
            logger.error(f"❌ El paso {i} falló: {script}")
            print("\n" + "="*70)
            print(f"❌ Pipeline interrumpido en el paso {i}/{len(steps)}")
            print("="*70)
            return 1

        logger.info(f"✓ Paso {i}/{len(steps)} completado exitosamente")

    # Resumen final
    duration = time.time() - start_time

    logger.info("="*70)
    logger.info("✓ Pipeline ETL completado exitosamente")
    logger.info(f"Duración total: {duration:.2f} segundos")
    logger.info("="*70)

    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*15 + "✓ PIPELINE COMPLETADO EXITOSAMENTE" + " "*19 + "║")
    print("╚" + "═"*68 + "╝")
    print(f"\n⏱  Duración total: {duration:.2f} segundos ({duration/60:.1f} minutos)")
    print("\n📊 Archivos generados:")
    print("   - data/output/salida_bugs.csv")
    print("   - data/output/salida_delivs.csv")
    print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
