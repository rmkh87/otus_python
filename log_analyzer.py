#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging

from classes.analyzer import LogAnalyzer
from utils.common import load_configs, apply_configs, set_logs_configs

logger = logging.getLogger(__name__)
set_logs_configs(logging)

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

# ARG params
parser = argparse.ArgumentParser(description='Парсер логов')
parser.add_argument(
    '--config',
    dest='config',
    default=None,
    required=False,
    help='Путь к конфигу (в env формате, шаблон .config_template)'
)

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./logs",
}


def main():
    logger.info("Старт")

    args = parser.parse_args()
    config_path = args.config
    if config_path:
        load_configs(config_path)
        set_logs_configs(logging)
        apply_configs(config)

    analyzer = LogAnalyzer(config)
    analyzer.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.exception('Process interrupted')
        raise
    except Exception as e:
        logger.exception(e)
        raise