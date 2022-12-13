import re
import logging
import os
import gzip
from datetime import datetime, date
from typing import Tuple

from configs.const import PARCING_ERROR_LIMIT_PERCENT
from app_types import TypeLogFile


logger = logging.getLogger(__name__)


def parse_log_line(text: str) -> Tuple[str, float]:
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


def get_date_from_filename(filename) -> date:
    try:
        filename_dt_str = re.search(r'(?<=log-)\d+', filename)[0]
        if filename_dt_str.isdigit():
            return datetime.strptime(
                '/'.join([
                    filename_dt_str[:4],
                    filename_dt_str[4:6],
                    filename_dt_str[6:8]
                ]),
                '%Y/%m/%d'
            )

    except Exception:
        return None

    return None


def get_last_log_file(log_dir: str) -> TypeLogFile:
    result = TypeLogFile(None, None, None)

    if not (os.path.isdir(log_dir) and os.listdir(log_dir)):
        return result

    name, name_dt = max(
        ((filename, get_date_from_filename(filename)) for filename in os.listdir(log_dir)),
        key=lambda _: _[-1]
    )

    return TypeLogFile(f'{log_dir}/{name}', name, name_dt)


def file_open_func(filename: str) -> open:
    ext = filename.split('.')[-1].lower()
    if ext == 'gz':
        return gzip.open
    return open


def read_file(file) -> str:
    for line in file:
        yield line


def read_log_file(file: TypeLogFile) -> dict:
    count_records = 0
    parcing_limit_error = 0
    log_data = {}

    open_func = file_open_func(file.name)

    logger.info(f"Чтение лога {file.name}...")
    with open_func(file.path, 'rt', encoding='utf-8') as file:
        for text in read_file(file):
            count_records += 1
            url, request_time = parse_log_line(text)

            if not url or not request_time:
                parcing_limit_error += 1
                continue

            if url not in log_data.keys():
                log_data[url] = []
            log_data[url].append(request_time)

    # Кол-во ошибок парсинга первысило лимит
    if parcing_limit_error:
        parcing_error_percent = int(100 * parcing_limit_error / count_records)
        if parcing_error_percent > PARCING_ERROR_LIMIT_PERCENT:
            logger.exception(
                f"Большую часть лога не удалось распарсить, превышен порог ошибок: {parcing_error_percent}%",
                exc_info=False
            )
            return {}

    return log_data
