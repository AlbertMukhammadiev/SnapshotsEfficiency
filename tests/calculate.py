from unittest import TestCase, main

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from efficiency import calculate

class CalculateTestCase(TestCase):
    def setUp(self):
        """initial set up"""
        pass

    def test_cow_efficiency(self):
        """Verify the correctness of counting migrating subblocks
        
        and the ratio of occupied logical blocks to physical ones.
        """
        migrtns, ratio = calculate.cow_efficiency('tests/sequential.csv', 10)
        migrtns2, ratio2 = calculate.cow_efficiency('tests/sequential.csv', 5)
        self.assertEqual(migrtns, migrtns2)
        self.assertEqual(migrtns, 91)
        self.assertAlmostEqual(ratio, 4 / 14)
        self.assertAlmostEqual(ratio2, 4 / 8)

        migrtns, ratio = calculate.cow_efficiency('tests/normal.csv', 10)
        migrtns2, ratio2 = calculate.cow_efficiency('tests/normal.csv', 5)
        self.assertEqual(migrtns, migrtns2)
        self.assertEqual(migrtns, 70)
        self.assertAlmostEqual(ratio, 4 / 26)
        self.assertAlmostEqual(ratio2, 4 / 14)

        migrtns, ratio = calculate.cow_efficiency('tests/uniform.csv', 10)
        self.assertEqual(migrtns, 52)
        self.assertAlmostEqual(ratio, 4 / 37)

    def test_row_efficiency(self):
        """Verify the correctness of counting migrating subblocks
        
        and the ratio of occupied logical blocks to physical ones.
        """
        migrtns, ratio = calculate.row_efficiency('tests/uniform.csv', 10,
                                                  modified=False)
        self.assertEqual(migrtns, 40)
        self.assertAlmostEqual(ratio, 4 / 37)

        migrtns, ratio = calculate.row_efficiency('tests/sequential.csv', 5,
                                                  modified=False)
        self.assertAlmostEqual(ratio, 4 / 10)

        # pre-calculated migrtns
        migrtns = [8, 20, 40, 61, 88, 117, 150, 184, 219, 255, 291]
        for i in range(11):
            n, _ = calculate.row_efficiency('tests/sequential.csv', 18 - i,
                                            modified=False)
            self.assertEqual(n, migrtns[i])

        migrtns, ratio = calculate.row_efficiency('tests/normal.csv', 10,
                                                  modified=False)
        self.assertAlmostEqual(ratio, 4 / 27, places=2)

        # pre-calculated migrtns
        migrtns = [7, 21, 41, 65, 92, 122, 155, 189, 225, 263, 306]
        for i in range(11):
            n, _ = calculate.row_efficiency('tests/normal.csv', 15 - i,
                                            modified=False)
            self.assertEqual(n, migrtns[i])

    def test_row_m_efficiency(self):
        """Verify the correctness of counting migrating subblocks
        
        and the ratio of occupied logical blocks to physical ones.
        """
        migrtns, ratio = calculate.row_efficiency('tests/sequential.csv', 8,
                                                  modified=True)
        self.assertEqual(migrtns, 78)
        self.assertAlmostEqual(ratio, 4 / 16)
        
        migrtns, ratio = calculate.row_efficiency('tests/normal.csv', 8,
                                                  modified=True)
        self.assertEqual(migrtns, 54)
        self.assertAlmostEqual(ratio, 4 / 29)

        migrtns, ratio = calculate.row_efficiency('tests/uniform.csv', 10,
                                                  modified=True)
        self.assertEqual(migrtns, 19)
        self.assertAlmostEqual(ratio, 4 / 38)
    

if __name__ == '__main__':
    main()