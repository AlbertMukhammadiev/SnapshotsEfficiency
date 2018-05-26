from unittest import TestCase, main
from numpy import zeros, count_nonzero

import distribute

class DistributeTestCase(TestCase):
    def setUp(self):
        """initial set up"""
        pass

    def test_sequential_occupied_count(self):
        """Verify function occupies correct number of cells"""
        space = zeros(128, dtype=bool)
        distribute.sequential(space, 70, 64)
        self.assertTrue(count_nonzero(space) == 64)

        space = zeros(128, dtype=bool)
        distribute.sequential(space, 64, 64)
        self.assertTrue(count_nonzero(space) == 64)

        space = zeros(128, dtype=bool)
        distribute.sequential(space, 0, 32)
        self.assertTrue(count_nonzero(space) == 32)

    def test_sequential_occupied_place(self):
        """Verify function occupies the cells in the right places"""
        space = zeros(128, dtype=bool)
        distribute.sequential(space, 70, 64)
        self.assertTrue(count_nonzero(space[:6]) == 6)
        self.assertTrue(count_nonzero(space[6:70]) == 0)
        self.assertTrue(count_nonzero(space[70:]) == 58)

        space = zeros(128, dtype=bool)
        distribute.sequential(space, 64, 64)
        self.assertTrue(count_nonzero(space[:64]) == 0)
        self.assertTrue(count_nonzero(space[64:]) == 64)

        space = zeros(128, dtype=bool)
        distribute.sequential(space, 0, 32)
        self.assertTrue(count_nonzero(space[:32]) == 32)
        self.assertTrue(count_nonzero(space[32:]) == 0)

    def test_uniform_occupied_count(self):
        """Verify function occupies correct number of cells"""
        space = zeros(128, dtype=bool)
        distribute.uniform(space, 64)
        self.assertTrue(count_nonzero(space) == 64)

        prev_state = space.copy()
        distribute.uniform_ow(space, 64, 16)
        self.assertTrue(count_nonzero(prev_state * space) == 16)
        self.assertTrue(count_nonzero(~prev_state * space) == 48)

        space = prev_state.copy()
        distribute.uniform_ow(space, 96, 80)
        self.assertTrue(count_nonzero(prev_state * space) == 64)
        self.assertTrue(count_nonzero(~prev_state * space) == 32)

if __name__ == '__main__':
    main()