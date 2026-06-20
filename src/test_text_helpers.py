import unittest

from text_helpers import remove_up_to_period


class MyTestCase(unittest.TestCase):
    def test_remove_up_to_period(self):
        line = "123. Blah blah blah"
        test = "Blah blah blah"
        after = remove_up_to_period(line)
        self.assertEqual(after, test)




if __name__ == '__main__':
    unittest.main()
