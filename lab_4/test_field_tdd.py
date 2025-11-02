import unittest
from field import field


class TestFieldTDD(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {'title': 'Ковер', 'price': 2000, 'color': 'green'},
            {'title': 'Диван для отдыха', 'color': 'black'},
            {'title': None, 'price': 1500},
            {'price': 3000},
            {'title': 'Стул', 'price': 800, 'color': 'white'}
        ]

    def test_single_argument_returns_values(self):
        result = list(field(self.test_data, 'title'))
        expected = ['Ковер', 'Диван для отдыха', 'Стул']
        self.assertEqual(result, expected)

    def test_multiple_arguments_returns_dicts(self):
        result = list(field(self.test_data, 'title', 'price'))
        expected = [
            {'title': 'Ковер', 'price': 2000},
            {'title': 'Диван для отдыха'},
            {'price': 1500},
            {'price': 3000},
            {'title': 'Стул', 'price': 800}
        ]
        self.assertEqual(result, expected)

    def test_none_values_are_skipped(self):
        result = list(field(self.test_data, 'color'))
        expected = ['green', 'black', 'white']
        self.assertEqual(result, expected)

    def test_empty_list_returns_empty(self):
        result = list(field([], 'title'))
        self.assertEqual(result, [])

    def test_no_valid_items_returns_empty(self):
        result = list(field([{'name': 'test'}], 'title'))
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()