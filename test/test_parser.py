import unittest
from utils.common import parse_log_line


class ParserTest(unittest.TestCase):
    def test(self):
        url, time = parse_log_line(''.join([
            '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] ',
            '"GET /api/v2/banner/25019354 HTTP/1.1" 200 927 ',
            '"-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 ',
            'GNUTLS/2.10.5" "-" ',
            '"1498697422-2190034393-4708-9752759" "dc7161be3" 0.390'
        ]))

        self.assertEqual(url, '/api/v2/banner/25019354')
        self.assertEqual(time, 0.390)

    def test_notequal(self):
        url, time = parse_log_line(''.join([
            '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] ',
            '"GET/api/v2/banner/25019354 HTTP/1.1" 200 927 ',
            '"-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 ',
            'GNUTLS/2.10.5" "-" ',
            '"1498697422-2190034393-4708-9752759" "dc7161be3" yt'
        ]))

        self.assertNotEqual(url, '/api/v2/banner/25019354')
        self.assertNotEqual(time, 0.390)


if __name__ == '__main__':
    unittest.main()
