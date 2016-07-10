from ..lib.utils import get_kpa
import unittest


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.temperature = 25
        self.kohms = 5.6

    def test_kpa_conversion(self):

        """ Test in the range of 1 < R < 8"""

        result = get_kpa(5.6, 25)

        self.assertTrue(result == -34.281679)

if __name__ == '__main__':
    unittest.main()
