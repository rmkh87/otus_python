import logging
from os import getenv

logger = logging.getLogger(__name__)


def load_configs(config_file: str):
    from os import path
    from dotenv import load_dotenv

    if not path.isfile(config_file):
        logger.exception("Ошибка при загрузке файла конфига: конфиг не найден")
        raise ValueError("Ошибка при загрузке файла конфига: конфиг не найден")

    load_dotenv(config_file)


def apply_configs(config: dict):
    report_size = getenv('REPORT_SIZE')
    if report_size:
        config['REPORT_SIZE'] = int(report_size)

    report_dir = getenv('REPORT_DIR')
    if report_dir:
        config['REPORT_DIR'] = report_dir

    log_dir = getenv('LOG_DIR')
    if log_dir:
        config['LOG_DIR'] = log_dir


def set_logs_configs(logging):
    logging.basicConfig(
        filename=getenv('APP_LOG', None),
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
    )
