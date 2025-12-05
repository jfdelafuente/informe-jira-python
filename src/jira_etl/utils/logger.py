"""Sistema de logging centralizado"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Directorio de logs
LOGS_DIR = Path(__file__).parent.parent.parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)


def setup_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> None:
    """
    Configura el sistema de logging para el proyecto.

    Args:
        log_file: Nombre del archivo de log (opcional, se genera automáticamente si no se proporciona)
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Formato personalizado para los mensajes de log
    """
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'jira_etl_{timestamp}.log'

    log_path = LOGS_DIR / log_file

    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Configurar logging
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Sistema de logging inicializado. Archivo: {log_path}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre especificado.

    Args:
        name: Nombre del logger (usualmente __name__)

    Returns:
        Objeto Logger configurado
    """
    return logging.getLogger(name)


def log(message: str) -> None:
    """
    Función legacy de logging para compatibilidad con código antiguo.

    DEPRECATED: Usar get_logger(__name__).info() en código nuevo.

    Args:
        message: Mensaje a registrar
    """
    logger = get_logger('legacy')
    logger.info(message)

    # Mantener archivo legacy para compatibilidad
    timestamp_format = '%H:%M:%S-%h-%d-%Y'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    legacy_log = Path('jira_bugs_logfile.txt')
    with open(legacy_log, "a", encoding='utf-8') as f:
        f.write(timestamp + ',' + message + '\n')
