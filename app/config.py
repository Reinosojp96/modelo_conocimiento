import os
from pathlib import Path

class Config:
    # Configuración de rutas
    BASE_DIR = Path(__file__).parent.parent
    INPUT_DIR = BASE_DIR / "input_pdfs"
    OUTPUT_DIR = BASE_DIR / "output"
    
    # Configuración de IA
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    MODEL_NAME = "gpt-4"  # o "gpt-3.5-turbo"
    
    # Límites de procesamiento
    MAX_FILE_SIZE_MB = 50
    MAX_TEXT_LENGTH = 8000  # para análisis por documento
    
    # Configuración de reportes
    REPORT_FORMATS = ['docx', 'txt']
    COMPANY_NAME = "Empresa Cliente"

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'processing.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}