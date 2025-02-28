# logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Configurar directorio de logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "api.log"

# Formato común
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str = "app") -> logging.Logger:
    """
    Configura un logger con manejo de archivos rotativos y consola.
    
    Args:
        name: Nombre del logger (por defecto 'app').

    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evitar logs duplicados
    if logger.handlers:
        return logger

    # Formato
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    # Handler para archivo (rotativo: 5 MB x 3 archivos)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Añadir handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Logger principal
logger = setup_logger()