import os
import logging

from time import time
from statistics import median
from functools import reduce
from string import Template

from app_types import TypeReport, TypeReportData


logger = logging.getLogger(__name__)


def get_report_filename(report: TypeReport) -> str:
    if not os.path.isdir(report.report_dir):
        logger.exception(f"Директория отчета {report.report_dir} не найдена")
        raise None

    filename = f'{report.report_dir}/report-{report.name_dt.strftime("%Y-%m-%d")}.html'
    if os.path.isfile(filename):
        return f'{report.report_dir}/report-{report.name_dt.strftime("%Y-%m-%d")}_{int(time())}.html'

    return filename


def get_report_data(url: str, times: [], time_sum: int, count_data: int, count_time_data: int) -> dict:
    data = dict({
        'url': url,
        'count': len(times),
        'time_sum': round(time_sum, 3),
        'time_max': max(times),
        'time_med': median(times),
    })

    data['time_avg'] = round(data['time_sum'] / data['count'], 3)
    data['count_perc'] = round((data['count'] * 100) / count_data, 3)
    data['time_perc'] = round((data['time_sum'] * 100) / count_time_data, 3)
    return data


def get_report_template(report_dir) -> Template:
    filename = f'{report_dir}/report.html'
    with open(filename, mode='r') as file:
        return Template(file.read())


def create_report(data: dict, size: int) -> TypeReportData:
    count = len(data.keys())
    if not count:
        return TypeReportData(0, 0, ())

    data = tuple(map(lambda _: (_[0], _[1], sum(_[1])), data.items()))
    count_time = reduce(lambda counter, item: counter + item[-1], data, 0)

    # сортировка по time_sum и получение первых report_size
    return TypeReportData(
        count_total=count,
        count_time=count_time,
        items=sorted(data, key=lambda _: _[-1], reverse=True)[:size]
    )


def save_report(report: TypeReport, data: TypeReportData):
    filename = get_report_filename(report)

    with open(filename, mode='w', encoding='utf-8') as file:
        table_json = (
            get_report_data(
                url=url,
                times=times,
                time_sum=time_sum,
                count_data=data.count_total,
                count_time_data=data.count_time,
            ) for url, times, time_sum in data.items
        )

        template = get_report_template(report.report_dir)
        file.write(template.safe_substitute(table_json=list(table_json)))

    logger.info(f"Отчет сохранен в файле: {filename}")
