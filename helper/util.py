import json
import logging.config
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def init_logger(default_level: str = logging.ERROR):
    logging_file_path = get_path('config') + 'logging.json'
    setup_logging(path=logging_file_path, default_level=default_level)


def setup_logging(path, default_level, env_key='LOG_CFG'):
    """Setup logging configuration"""
    value = os.getenv(env_key, None)
    if value:
        path = value
    logger.info('Reading logging _config from {0}'.format(path))
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logger.info('Not found! Using basic logging configuration...')
        logging.basicConfig(level=default_level)


def get_path(folder_name: str = None):
    root_path = str(Path(__file__).parents[1])
    found_path = None
    result = None
    if folder_name:
        for r, d, f in os.walk(root_path):
            for folder in d:
                if folder == folder_name:
                    found_path = r
                    break
        if found_path:
            result = found_path + '\\' + folder_name + '\\'
    else:
        result = root_path
    return result


def string_2_bool(string_2_convert):
    result = False
    if string_2_convert:
        if string_2_convert.lower() == 'true':
            result = True
    return result