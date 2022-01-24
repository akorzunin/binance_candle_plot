import unittest
from modules.logic_modules.alg_checker import AlgChecker
class TestAlgMethods(unittest.TestCase):


    def test_checker(self):
        a = AlgChecker()
        self.assertEqual(a.check(), False)

    def test_isupper(self):
        self.assertTrue('ADJLH'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()