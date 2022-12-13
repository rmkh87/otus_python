import unittest
from functools import reduce

from utils.report import create_report


class ParserTest(unittest.TestCase):
    def test_create_report(self):
        data = {
            '/api/v2/banner/25019354': [0.39],
            '/api/1/photogenic_banners/list/?server_name=WIN7RB4': [0.133],
            '/api/v2/banner/16852664': [0.199],
            '/api/v2/slot/4705/groups': [0.704],
        }
        data_tuple = tuple(map(lambda _: (_[0], _[1], sum(_[1])), data.items()))

        result = create_report(data=data, size=10)

        self.assertEqual(len(data_tuple), result.count_total)
        self.assertEqual(reduce(lambda counter, item: counter + item[-1], data_tuple, 0), result.count_time)
        self.assertEqual(4, len(result.items))


if __name__ == '__main__':
    unittest.main()
