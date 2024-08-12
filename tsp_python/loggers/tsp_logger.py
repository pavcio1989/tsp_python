import logging
from logging.config import dictConfig
from typing import Optional, Union


class TSPLogger:
    def __init__(self, name: str, level: Union[str, int] = logging.INFO):
        self._logger: Optional[logging.Logger] = None
        self._initialize_logger(name=name, level=level)

    def _get_logger_config(self, name, level):
        return dict(
            version=1,
            disable_existing_loggers=False,
            formatters={
                "standard": {
                    "format": '%(asctime)s [%(levelname)s] %(name)s: %(message)s\n'
                },
            },
            handlers={
                'default': {
                    'level': "INFO",
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',  # Default is stderr
                },
                'file': {
                    'level': "WARNING",
                    'formatter': 'standard',
                    'class': 'logging.FileHandler',
                    'mode': 'w',
                    'filename': 'logs/log.log'
                },
            },
            loggers={
                name: {
                    'handlers': ['default', 'file'],
                    'level': level,
                    'propagate': False
                },
                'tsp': {
                    'handlers': ['default', 'file'],
                    'level': level,
                    'propagate': False
                }
            }
        )

    def _initialize_logger(self, name, level):
        dictConfig(self._get_logger_config(name, level))
        logger = logging.getLogger(name)
        self._logger = logger
