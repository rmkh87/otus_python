import os
import re
import gzip
import logging
import time
from datetime import datetime

from classes.parcer import LogParcer
from classes.report import LogReport
from configs.const import PARCING_ERROR_LIMIT_PERCENT

logger = logging.getLogger(__name__)


class AnalyzerBase:
    def _get_date_from_filename(self, filename):
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

    def _find_last_log_file(self):
        if not os.path.isdir(self.log_dir):
            logger.exception(f"Директория лога {self.log_dir} не найдена")
            raise ValueError(f"Директория лога {self.log_dir} не найдена")

        filename_result = None
        filename_dt_max = None

        for filename in os.listdir(self.log_dir):
            filename_dt = self._get_date_from_filename(filename)

            if filename_dt:
                if not filename_result:
                    filename_result = filename
                if not filename_dt_max:
                    filename_dt_max = filename_dt

                if filename_dt_max < filename_dt:
                    filename_result = filename
                    filename_dt_max = filename_dt

        if filename_result:
            return filename_result, filename_result.split('.')[-1].lower(), filename_dt_max

        return None, None, None

    def _read_file(self, file):
        while True:
            data = file.readline()
            if not data:
                break
            yield data

    def _file_open_func(self, extension):
        if extension == 'gz':
            return gzip.open
        return open

    def run(self):
        raise NotImplementedError


class LogAnalyzer(AnalyzerBase):
    log_dir: str = './logs'
    report_size: int = 0
    report_dir: str = ''
    parcing_limit_error = 0

    def __init__(self, config: dict = {}):
        self.log_dir = config.get('LOG_DIR')
        self.report_size = config.get('REPORT_SIZE')
        self.report_dir = config.get('REPORT_DIR')

        if not (self.log_dir and self.report_size and self.report_dir):
            logger.exception("Ошибка: не указаны конфиги")
            raise ValueError("Ошибка: не указаны конфиги")

    def run(self):
        count_records = 0
        start_execute = time.time()

        filename, filename_ext, filename_dt = self._find_last_log_file()
        if not filename:
            logger.exception("Файл логов не найден", exc_info=False)
            return

        filename = f'{self.log_dir}/{filename}'

        # parce log file
        logger.info(f"Чтение лога {filename}...")
        log_data = {}
        log_parcer = LogParcer()

        open_func = self._file_open_func(filename_ext)
        with open_func(filename, 'rt') as file:
            for text in self._read_file(file):
                count_records += 1
                url, request_time = log_parcer.parce(text)

                if not url or not request_time:
                    self.parcing_limit_error += 1
                    continue

                if url not in log_data.keys():
                    log_data[url] = []
                log_data[url].append(request_time)

        # Кол-во ошибок парсинга первысило лимит
        if self.parcing_limit_error:
            parcing_error_percent = int(100 * self.parcing_limit_error / count_records)
            if parcing_error_percent > PARCING_ERROR_LIMIT_PERCENT:
                logger.exception(
                    f"Большую часть лога не удалось распарсить, превышен порог ошибок: {parcing_error_percent}%",
                    exc_info=False
                )
                return

        if not log_data.keys():
            logger.info("Данные в логе не прочитаны или лог пустой")
            return

        # make report from log data
        log_report = LogReport(
            report_size=self.report_size,
            report_dir=self.report_dir,
            report_dt=filename_dt,
        )
        log_report.make_report(log_data)

        logger.info("Время выполнения: %s сек.", round(time.time() - start_execute, 3))
