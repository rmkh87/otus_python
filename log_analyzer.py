import argparse
import logging
import os
import configparser
from time import time

from utils.analyze import get_last_log_file, read_log_file
from utils.report import save_report, create_report
from app_types import TypeLogFile, TypeReport


logger = logging.getLogger(__name__)

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

# ARG params
parser = argparse.ArgumentParser(description='Парсер логов')
parser.add_argument(
    '--config',
    dest='config',
    default='./settings.ini',
    required=False,
    help='Путь к конфигу (в ini формате)'
)

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./logs",
}


def load_configs(config_file: str, config: dict):
    if not os.path.isfile(config_file):
        raise Exception("Ошибка при загрузке файла конфига: конфиг не найден")

    config_load = configparser.ConfigParser()
    config_load.read(config_file)

    for key, value in config_load["Common"].items():
        if value.isdigit():
            value = int(value)
        config[key.upper()] = value


def init():
    args = parser.parse_args()
    config_path = args.config

    load_configs(config_path, config)

    logging.basicConfig(
        filename=config.get('APP_LOG', None),
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
    )


def main(config):
    file: TypeLogFile = get_last_log_file(config.get('LOG_DIR'))
    if not file.name:
        raise Exception("Файл логов не найден")

    log_data = read_log_file(file)
    if not log_data.keys():
        raise Exception("Данные в логе не прочитаны или лог пустой")

    report_data = create_report(data=log_data, size=config.get('REPORT_SIZE'))
    save_report(
        report=TypeReport(report_dir=config.get('REPORT_DIR'), name_dt=file.name_dt),
        data=report_data
    )


if __name__ == "__main__":
    start_execute = time()

    try:
        init()
        main(config)

    except (KeyboardInterrupt, SystemExit):
        logger.exception('Process interrupted')

    except Exception as e:
        logger.exception(e)

    finally:
        logger.info("Время выполнения: %s сек.", round(time() - start_execute, 3))
