import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'f': {
            'format':
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    handlers={
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.DEBUG
        }
    },
    loggers={
        'threescale_api': {
            'handlers': ['h'],
            'level': logging.DEBUG
        },
        'tests': {
            'handlers': ['h'],
            'level': logging.DEBUG
        }
    },
)


def load_config():
    dictConfig(logging_config)
