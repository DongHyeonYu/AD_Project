import unittest

from loadXlsx import LoadXlsx


class TestPalindrome(unittest.TestCase):

    def setUp(self):
        self.p1 = LoadXlsx("지하수로")
    def tearDown(self):
        pass
    def testLoadXlsx(self):
        self.assertTrue(self.p1.getName(),['test1','test4','test7','test2','test5','test8','test3','test6','test9'])

if __name__ == '__main__':
    unittest.main()
