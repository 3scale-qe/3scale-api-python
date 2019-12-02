import logging
from logging.config import dictConfig

#LEVEL=logging.DEBUG
LEVEL=logging.INFO

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
            'level': LEVEL
        }
    },
    loggers={
        'threescale_api': {
            'handlers': ['h'],
            'level': LEVEL
        },
        'tests': {
            'handlers': ['h'],
            'level': LEVEL
        }
    },
)


def load_config():
    dictConfig(logging_config)
