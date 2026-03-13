import unittest
from my_func import my_multisets_intersection


class TestMyMultisetsIntersection(unittest.TestCase):

    def test_both_empty(self):
        """Пустое множество
        """
        self.assertCountEqual(my_multisets_intersection([], []), [])

    def test_one_empty(self):
        """Одно пустое множество
        """
        self.assertCountEqual(my_multisets_intersection([1, 2], []), [])
        self.assertCountEqual(my_multisets_intersection([], [1, 2]), [])

    def test_no_common_elements(self):
        """Нет пересечений
        """
        self.assertCountEqual(my_multisets_intersection([1, 2, 3], [4, 5, 6]), [])

    def test_identical_lists(self):
        """Одинаковые множества
        """
        self.assertCountEqual(my_multisets_intersection([1, 2, 2, 3], [1, 2, 2, 3]), [1, 2, 2, 3])
        self.assertCountEqual(my_multisets_intersection([3, 2, 2, 3], [2, 3, 2, 3]), [2, 2, 3, 3])

    def test_different_counts(self):
        """Разный размер множеств
        """
        self.assertCountEqual(my_multisets_intersection([1, 1, 1, 2], [1, 1, 3]), [1, 1])
        self.assertCountEqual(my_multisets_intersection([1, 1], [1, 1, 1]), [1, 1])
        self.assertCountEqual(my_multisets_intersection([3, 2, 2, 3], [1, 2, 3, 2, 3]), [2, 2, 3, 3])


if __name__ == '__main__':
    unittest.main(verbosity=3)
    