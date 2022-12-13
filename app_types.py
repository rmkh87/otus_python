from collections import namedtuple


TypeLogFile = namedtuple('TypeLogFile', ['path', 'name', 'name_dt'])
TypeReportData = namedtuple('TypeReportData', ['count_total', 'count_time', 'items'])
TypeReport = namedtuple('TypeReport', ['report_dir', 'name_dt'])
