from unittest import TestCase, main
from collections import deque
from numpy import array, array_equal
from functools import partial

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from efficiency import migrations

bool_array = partial(array, dtype=bool)

class MigrationsTestCase(TestCase):
    def setUp(self):
        """initial set up"""
        self.snapshots1 = deque(
            [
                bool_array([1,1,0,1,1,0,1,0]),
                bool_array([0,1,0,0,0,0,0,0]),
                bool_array([0,0,1,0,0,0,0,0]),
                bool_array([0,0,0,0,0,0,0,0]),
                bool_array([0,0,0,0,1,0,0,0]),
                bool_array([0,0,0,0,0,1,0,0]),
                bool_array([0,0,0,0,0,0,0,1])
            ],
            maxlen=7
        )

        self.snapshots2 = deque(
            [
                bool_array([1,1,1,1,1,1,0,0]),
                bool_array([1,0,0,0,0,1,0,0]),
                bool_array([0,1,0,0,1,0,0,0]),
                bool_array([0,0,1,0,0,0,1,0]),
                bool_array([0,0,0,1,0,0,0,1]),
                bool_array([0,0,0,0,0,0,0,0]),
                bool_array([0,0,1,1,0,0,0,0])
            ],
            maxlen=7
        )

        self.snapshots3 = deque(
            [
                bool_array([1,0,0,0,0,0,0,1]),
                bool_array([0,1,0,0,0,0,0,0]),
                bool_array([0,0,1,0,0,0,0,0]),
                bool_array([0,0,0,1,0,0,0,0]),
                bool_array([0,0,0,0,1,0,0,0]),
                bool_array([0,0,0,0,0,1,0,0]),
                bool_array([0,0,0,0,0,0,1,0])
            ],
            maxlen=7
        )

        self.snapshots4 = deque(
            [
                bool_array([1,0,1,0,0,0,0,1]),
                bool_array([0,0,1,1,0,1,0,0]),
                bool_array([0,1,0,0,1,0,1,0])
            ],
            maxlen=4
        )

        self.snapshots5 = deque(
            [
                bool_array([0,0,0,0,0,0,0,0]),
                bool_array([0,1,0,1,0,0,0,1]),
                bool_array([0,0,1,0,1,0,1,0]),
                bool_array([1,0,0,0,0,1,0,0])
            ],
            maxlen=4
        )

        self.snapshots6 = deque(
            [
                bool_array([1,0,1,0,1,0,1,0]),
                bool_array([1,1,0,1,1,0,1,1]),
                bool_array([0,0,1,0,0,0,0,0]),
                bool_array([0,0,0,1,0,0,0,0]),
                bool_array([0,0,0,0,1,0,0,0]),
                bool_array([0,0,0,0,0,1,0,0]),
                bool_array([0,0,0,0,0,0,1,0]),
                bool_array([0,0,0,0,0,0,0,1]),
                bool_array([1,0,0,0,0,0,0,0]),
                bool_array([0,1,0,0,0,0,0,0]),
                bool_array([0,0,1,0,0,0,0,0]),
                bool_array([0,0,0,1,0,0,0,0]),
                bool_array([0,0,0,0,1,0,0,0]),
                bool_array([0,0,0,0,0,1,0,0]),
                bool_array([0,0,0,0,0,0,1,0]),
                bool_array([0,0,0,0,0,0,0,1])
            ],
            maxlen=16
        )


    def test_cow(self):
        """Verify the correctness of counting migrating subblocks"""
        source_block = bool_array([1,0,0,1,1,0,0,1,0,1])
        new_block = bool_array([0,0,1,0,1,1,0,0,1,1])
        self.assertEqual(migrations.cow(source_block, new_block), 2)

        source_block = bool_array([1,0,0,1,1,0,0,1,0,1])
        new_block = bool_array([0,1,1,0,0,1,1,0,1,0])
        self.assertEqual(migrations.cow(source_block, new_block), 0)

        source_block = bool_array([0,0,0,0,0,0,0,0,0,0])
        new_block = bool_array([0,0,1,0,1,1,0,0,1,1])
        self.assertEqual(migrations.cow(source_block, new_block), 0)


    def test_row(self):
        """Verify the correctness of counting migrating subblocks"""
        previous_state = list(self.snapshots1)
        self.assertEqual(migrations.row(self.snapshots1), 4)
        self.assertEqual(len(self.snapshots1), 7)
        indices = [0, 3, 4, 6]
        previous_state[0][indices] = False
        previous_state[1][indices] = True
        for snap1, snap2 in zip(previous_state, self.snapshots1):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots2.copy()
        self.assertEqual(migrations.row(self.snapshots2), 4)
        self.assertEqual(len(self.snapshots2), 7)
        indices = [1, 2, 3, 4]
        previous_state[0][indices] = False
        previous_state[1][indices] = True
        for snap1, snap2 in zip(previous_state, self.snapshots2):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots3.copy()
        self.assertEqual(migrations.row(self.snapshots3), 2)
        indices = [0, 7]
        previous_state[0][indices] = False
        previous_state[1][indices] = True
        self.assertEqual(len(self.snapshots3), 7)
        for snap1, snap2 in zip(previous_state, self.snapshots3):
            self.assertTrue(array_equal(snap1, snap2))
        
        previous_state = self.snapshots4.copy()
        self.assertEqual(migrations.row(self.snapshots4), 0)
        self.assertEqual(len(self.snapshots4), 3)
        for snap1, snap2 in zip(previous_state, self.snapshots4):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots5.copy()
        self.assertEqual(migrations.row(self.snapshots5), 0)
        self.assertEqual(len(self.snapshots5), 4)
        for snap1, snap2 in zip(previous_state, self.snapshots5):
            self.assertTrue(array_equal(snap1, snap2))


    def test_row_m(self):
        """Verify the correctness of counting migrating subblocks"""
        previous_state = list(self.snapshots1)
        self.assertEqual(migrations.row_m(self.snapshots1), 4)
        self.assertEqual(len(self.snapshots1), 7)
        previous_state[0][[0, 3, 4, 6]] = False
        previous_state[3][4] = True
        previous_state[6][[0, 3, 6]] = True
        for snap1, snap2 in zip(previous_state, self.snapshots1):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots2.copy()
        self.assertEqual(migrations.row_m(self.snapshots2), 4)
        self.assertEqual(len(self.snapshots2), 7)
        previous_state[0][[1, 2, 3, 4]] = False
        previous_state[1][[1, 4]] = True
        previous_state[2][2] = True
        previous_state[3][3] = True
        for snap1, snap2 in zip(previous_state, self.snapshots2):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots6.copy()
        self.assertEqual(migrations.row_m(self.snapshots6), 1)
        self.assertEqual(len(self.snapshots6), 16)
        previous_state[0][2] = False
        previous_state[1][2] = True
        for snap1, snap2 in zip(previous_state, self.snapshots6):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots3.copy()
        self.assertEqual(migrations.row_m(self.snapshots3), 2)
        self.assertEqual(len(self.snapshots3), 7)
        previous_state[0][[0, 7]] = False
        previous_state[6][[0, 7]] = True
        for snap1, snap2 in zip(previous_state, self.snapshots3):
            self.assertTrue(array_equal(snap1, snap2))
        
        previous_state = self.snapshots4.copy()
        self.assertEqual(migrations.row_m(self.snapshots4), 0)
        self.assertEqual(len(self.snapshots4), 3)
        for snap1, snap2 in zip(previous_state, self.snapshots4):
            self.assertTrue(array_equal(snap1, snap2))

        previous_state = self.snapshots5.copy()
        self.assertEqual(migrations.row_m(self.snapshots5), 0)
        self.assertEqual(len(self.snapshots5), 4)
        for snap1, snap2 in zip(previous_state, self.snapshots5):
            self.assertTrue(array_equal(snap1, snap2))


if __name__ == '__main__':
    main()