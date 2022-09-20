import unittest
from classes.analyzer import LogAnalyzer
from tempfile import TemporaryDirectory, NamedTemporaryFile


class ParcerTest(unittest.TestCase):
    def test_init(self):
        try:
            LogAnalyzer()
        except ValueError:
            pass
        else:
            self.fail('Тест на ValueError не пройден')

    def test_find_file(self):
        with TemporaryDirectory() as dir_logs:
            config = {
                "REPORT_SIZE": 1,
                "REPORT_DIR": dir_logs,
                "LOG_DIR": dir_logs,
            }
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

            analyzer = LogAnalyzer(config)
            filename, _, _ = analyzer._find_last_log_file()

            filename = f'{dir_logs}/{filename}'

            self.assertEqual(filename, fp_last.name)


if __name__ == '__main__':
    unittest.main()
