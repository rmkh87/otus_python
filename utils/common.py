import re
import logging
import configparser
from os import path

logger = logging.getLogger(__name__)


def load_configs(config_file: str, config: dict):
    if not path.isfile(config_file):
        logger.exception("Ошибка при загрузке файла конфига: конфиг не найден")
        raise ValueError("Ошибка при загрузке файла конфига: конфиг не найден")

    config_load = configparser.ConfigParser()
    config_load.read(config_file)

    for key, value in config_load["Common"].items():
        if value.isdigit():
            value = int(value)
        config[key.upper()] = value


def set_logs_configs(logging, config: dict):
    logging.basicConfig(
        filename=config.get('APP_LOG', None),
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
    )


def parse_log_line(text: str):
    url = None
    time = None

    pattern = r'(?:GET|POST|PUT|DELETE|PATCH|OPTIONS) /\S*'
    match = re.search(pattern, text)
    if match:
        url = match[0].split(' ')[-1]

    text_list = text.split(' ')
    request_time = text_list[-1].strip()
    if request_time.replace('.', '').isdigit():
        time = float(request_time)

    return url, time
