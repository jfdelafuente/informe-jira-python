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
from jira_etl.etl.transform import Data_Quality

# Intentar importar colorama para colores
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORS = True
except ImportError:
    HAS_COLORS = False
    class Fore:
        GREEN = CYAN = YELLOW = RED = WHITE = MAGENTA = ""
    class Style:
        BRIGHT = RESET_ALL = DIM = ""


class OutputManager:
    """Gestor centralizado de salida con colores y thread-safety"""

    def __init__(self, use_colors=True):
        self.use_colors = use_colors and HAS_COLORS
        self.lock = Lock()  # Para thread-safety en prints

    def _print(self, msg, color="", style=""):
        """Print thread-safe con colores opcionales"""
        with self.lock:
            if self.use_colors and color:
                print(f"{color}{style}{msg}{Style.RESET_ALL}")
            else:
                print(msg)

    def header(self, text):
        """Imprime encabezado"""
        sep = "=" * 60
        if self.use_colors:
            self._print(f"\n{sep}", Fore.CYAN, Style.BRIGHT)
            self._print(text, Fore.CYAN, Style.BRIGHT)
            self._print(sep, Fore.CYAN, Style.BRIGHT)
        else:
            self._print(f"\n{sep}")
            self._print(text)
            self._print(sep)

    def section(self, text):
        """Imprime sección"""
        self._print(f"[+] {text}", Fore.YELLOW, Style.BRIGHT)

    def success(self, text):
        """Mensaje de éxito"""
        self._print(f"  [OK] {text}", Fore.GREEN)

    def skip(self, text):
        """Mensaje de skip"""
        self._print(f"  [SKIP] {text}", Fore.YELLOW)

    def error(self, text):
        """Mensaje de error"""
        self._print(f"  [ERROR] {text}", Fore.RED)

    def info(self, text):
        """Mensaje informativo"""
        self._print(f"{text}", Fore.CYAN)

    def progress(self, current, total, incidencia, bugs, status="OK"):
        """Muestra progreso con formato consistente"""
        percentage = (current / total * 100) if total > 0 else 0

        if status == "OK":
            color = Fore.GREEN
            symbol = "[OK]"
        elif status == "SKIP":
            color = Fore.YELLOW
            symbol = "[SKIP]"
        else:
            color = Fore.RED
            symbol = "[ERROR]"

        msg = f"  {symbol} [{current}/{total}] {incidencia}: {bugs} bugs ({percentage:.1f}%)"
        self._print(msg, color)

    def summary(self, stats: Dict[str, Any]):
        """Imprime resumen final"""
        duration = stats.get('duration', 0)
        processed = stats.get('processed', 0)
        success = stats.get('success', 0)
        failed = stats.get('failed', 0)
        total_bugs = stats.get('total_bugs', 0)
        throughput = processed / duration if duration > 0 else 0

        self.header("RESUMEN FINAL")
        self.info(f"  Incidencias procesadas: {processed}")
        self.info(f"  Archivos generados: {Fore.GREEN}{success}{Style.RESET_ALL if self.use_colors else ''}")
        self.info(f"  Fallidos: {Fore.RED}{failed}{Style.RESET_ALL if self.use_colors else ''}")
        self.info(f"  Total bugs encontrados: {total_bugs}")
        self.info(f"  Duracion: {duration:.2f} segundos")
        self.info(f"  Rendimiento: {throughput:.2f} inc/seg")
        self.info(f"  Ubicacion: {Config.BUGS_JSON_DIR}")


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

        # Logging final
        logger.info("="*60)
        logger.info(f"Proceso completado: {results['success']} archivos generados")
        logger.info(f"Exitosos: {results['success']}, Fallidos: {results['failed']}")
        logger.info(f"Total bugs encontrados: {results['total_bugs']}")
        logger.info(f"Duración: {duration:.2f} segundos")
        logger.info("="*60)

        # Mostrar resumen
        output.summary(results)

        return 0

    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        output.error(f"ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
