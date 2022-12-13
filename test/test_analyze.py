import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

from utils.analyze import (
    read_log_file,
    get_last_log_file,
    parse_log_line,
)


class AnylyzeTest(unittest.TestCase):

    def test_get_last_log_file(self):
        with TemporaryDirectory() as dir_logs:
            config = {"REPORT_SIZE": 1, "REPORT_DIR": dir_logs, "LOG_DIR": dir_logs}
            NamedTemporaryFile(
                dir=dir_logs,
                suffix='_nginx-access-ui.log-20210929',
                delete=False,
            )
            fp_last = NamedTemporaryFile(
                dir=dir_logs,
                suffix='_nginx-access-ui.log-20221004',
                delete=False,
            )

            file = get_last_log_file(config.get('LOG_DIR'))

            self.assertEqual(file.path, fp_last.name)

    def test_read_log_file(self):
        with TemporaryDirectory() as dir_logs:
            config = {"REPORT_SIZE": 1, "REPORT_DIR": dir_logs, "LOG_DIR": dir_logs}
            tmp_file = NamedTemporaryFile(
                dir=dir_logs,
                suffix='_nginx-access-ui.log-20210929',
                delete=False,
            )

            with open(tmp_file.name, 'w') as f:
                f.write("""1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390
1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" 0.133
""") # noqa: noqa

            file = get_last_log_file(config.get('LOG_DIR'))
            log_data = read_log_file(file=file)
            self.assertEqual(len(log_data.keys()), 2)

    def test_parse_log_line(self):
        url, time = parse_log_line(''.join([
            '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] ',
            '"GET /api/v2/banner/25019354 HTTP/1.1" 200 927 ',
            '"-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 ',
            'GNUTLS/2.10.5" "-" ',
            '"1498697422-2190034393-4708-9752759" "dc7161be3" 0.390'
        ]))

        self.assertEqual(url, '/api/v2/banner/25019354')
        self.assertEqual(time, 0.390)


if __name__ == '__main__':
    unittest.main()
