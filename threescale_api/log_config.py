import logging
from logging.config import dictConfig


def _to_log_level_map(log_map: dict) -> dict:
    result = {}
    for level, arr in log_map.items():
        for item in arr:
            result[item] = level
    return result


_LOG_LEVEL_MAP_DEFINITION = {
    logging.CRITICAL: ['critical', 'c', 'crit'],
    logging.ERROR: ['error', 'e', 'err'],
    logging.WARNING: ['warning', 'w', 'warn'],
    logging.INFO: ['info', 'i', 'inf'],
    logging.DEBUG: ['debug', 'd', 'dbg'],
    logging.NOTSET: ['notset', 'n', 'nst'],
}

LOG_LEVEL_MAP = _to_log_level_map(_LOG_LEVEL_MAP_DEFINITION)


def to_log_level(level: str, default=logging.NOTSET) -> int:
    if isinstance(level, int):
        return level

    if level is not None:
        return LOG_LEVEL_MAP.get(level.lower(), default)
    return default


def load_config(level: str = "INFO", handler_level=None, api_level=None, tests_level=None):
    config = dict(
        version=1,
        formatters={
            'verbose': {
                'format':
                    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'level': to_log_level(handler_level, default=level)
            }
        },
        loggers={
            'threescale_api': {
                'handlers': ['console'],
                'level': to_log_level(api_level, default=level)
            },
            'tests': {
                'handlers': ['console'],
                'level': to_log_level(handler_level, default=level)
            }
        },
    )

    dictConfig(config)
