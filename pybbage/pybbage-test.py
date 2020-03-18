import unittest
from pyb import pybbage as pyb

print(pyb.__file__)

class MyTestCase(unittest.TestCase):
    def trivial_test_deleteme(self):
        self.assertEqual(True, True)

    def test_cardstr_back(self):
        # should do a more thorough test, that in all cases from 0..51 this is so
        self.assertEqual(pyb.stringcard(pyb.cardstring(0)),0)


if __name__ == '__main__':
    unittest.main()
