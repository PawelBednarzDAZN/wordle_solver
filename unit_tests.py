import unittest

from next_move import matches_state
from consts import GREEN, YELLOW

class TestNextMove(unittest.TestCase):

    def test_empty_state(self):
        self.assertTrue(matches_state('kreta', []))

    def test_one_yellow(self):
        self.assertTrue(matches_state('kreta', [(0, 'r', YELLOW)]))

    def test_yellow_when_green_taken(self):
        self.assertTrue(matches_state('krata', [(2, 'a', GREEN), (0, 'a', YELLOW)]))

    def test_yellow_reshuffled(self):
        self.assertTrue(matches_state('pawel', [(0, 'w', YELLOW), (1, 'l', YELLOW),
            (2, 'e', YELLOW), (3, 'p', YELLOW), (4, 'a', YELLOW)]))

    def test_green_wrong(self):
        self.assertFalse(matches_state('krata', [(0, 'o', GREEN)]))

    def test_yellow_missing(self):
        self.assertFalse(matches_state('krata', [(0, 'o', YELLOW)]))

    def test_yellow_missing_when_green_fits(self):
            self.assertFalse(matches_state('krata', [(2, 'a', GREEN), (0, 'w', YELLOW)]))

if __name__ == '__main__':
    unittest.main()
