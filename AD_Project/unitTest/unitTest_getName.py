import unittest
from getName import PrintName
class TestLoadXlsx(unittest.TestCase):
    def setUp(self):
        self.p1 = PrintName("nameList.txt")

    def tearDown(self):
        pass

    def testGetName(self):
        self.assertTrue(self.p1.getNameList(), ['test1','test2','test3','test4','test5'])

if __name__ == '__main__':
    unittest.main()