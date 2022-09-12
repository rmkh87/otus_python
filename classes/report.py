import os
from functools import reduce
from datetime import datetime
from time import time
from string import Template
from statistics import median
import logging

logger = logging.getLogger(__name__)


class LogReport:
    report_size: int = 0
    report_dir: str = ''
    report_dt: datetime = None
    count_data: int = 0
    count_time_data: int = 0

    def __init__(self, report_size: int, report_dir: str, report_dt: datetime):
        logger.info("Формирование отчета...")

        self.report_size = report_size
        self.report_dir = report_dir
        self.report_dt = report_dt

    def make_report(self, data: dict):
        self.count_data = len(data.keys())
        self.count_time_data = 0

        report_data = tuple(map(lambda _: (_[0], _[1], sum(_[1])), data.items()))
        self.count_time_data = reduce(lambda counter, item: counter + item[-1], report_data, 0)

        # сортировка по time_sum и получение первых report_size
        report_data = sorted(report_data, key=lambda _: _[-1], reverse=True)[:self.report_size]

        # сохраняем отчет в файле
        self._save_report(report_data)

    def _save_report(self, report_data: tuple):
        logger.info("Сохранение отчета...")

        filename = self._get_report_filename()
        with open(filename, mode='w', encoding='utf-8') as file:
            table_json = (
                self._analyze(url, times, time_sum) for url, times, time_sum in report_data
            )

            template = self._get_template()
            file.write(template.safe_substitute(table_json=list(table_json)))

        logger.info(f"Отчет сохранен в файле: {filename}")

    def _analyze(self, url: str, times: [], time_sum):
        data = dict({
            'url': url,
            'count': len(times),
            'time_sum': round(time_sum, 3),
            'time_max': max(times),
            'time_med': median(times),
        })

        data['time_avg'] = round(data['time_sum'] / data['count'], 3)
        data['count_perc'] = round((data['count'] * 100) / self.count_data, 3)
        data['time_perc'] = round((data['time_sum'] * 100) / self.count_time_data, 3)
        return data

    def _get_template(self):
        filename = f'{self.report_dir}/report.html'
        with open(filename, mode='r') as file:
            return Template(file.read())

    def _get_report_filename(self):
        if not os.path.isdir(self.report_dir):
            logger.exception(f"Директория отчета {self.report_dir} не найдена")
            raise ValueError(f"Директория отчета {self.report_dir} не найдена")

        filename = f'{self.report_dir}/report-{self.report_dt.strftime("%Y-%m-%d")}.html'
        if os.path.isfile(filename):
            return f'{self.report_dir}/report-{self.report_dt.strftime("%Y-%m-%d")}_{int(time())}.html'

        return filename
