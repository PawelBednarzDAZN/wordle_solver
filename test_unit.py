import unittest

from next_move import matches_state, get_inclusions, get_letter_scores, get_scoring_keys, get_word_score, next_move, solved
from consts import GREEN, YELLOW, GREY, RED, WORD_SIZE, NO_POSITION

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

    def test_gray_constraint_can_exclude_word(self):
        self.assertFalse(matches_state('krata', [(NO_POSITION, 'k', GREY)]))

    def test_red_constraint_can_exclude_word(self):
        self.assertFalse(matches_state('kraty', [(NO_POSITION, 'a', RED)]))

    def test_exclude_green(self):
        self.assertEqual(get_inclusions([(0, 'w', GREEN)]), [1, 2, 3, 4])

    def test_dont_exclude_yellow(self):
        self.assertEqual(get_inclusions([(0, 'w', YELLOW) ]), range(WORD_SIZE))

    def test_inclusions_in_mixed_setup(self):
        self.assertEqual(get_inclusions([(0, 'w', GREEN), (1, 'r', YELLOW), (2, 'e', GREEN), (4, 'a', GREEN)]), [1, 3])

    def test_scoring_keys(self):
        self.assertEqual(get_scoring_keys('kreta', [1, 3]), ['r0', 't0'])

    def test_scoring_keys(self):
        self.assertEqual(get_scoring_keys('krata', [2, 4]), ['a0', 'a1'])

    def test_scoring_keys(self):
        self.assertItemsEqual(get_scoring_keys('agata', [0, 2, 3, 4]), ['a0', 'a1', 't0', 'a2'])

    def test_lscores_full_inclusions_singles(self):
        result = get_letter_scores(['words'], [0, 1, 2, 3, 4])
        self.assertEqual(result['w0'], 1)
        self.assertEqual(result['o0'], 1)
        self.assertEqual(result['r0'], 1)
        self.assertEqual(result['d0'], 1)
        self.assertEqual(result['s0'], 1)

    def test_lscores_full_inclusions_repetitions(self):
        result = get_letter_scores(['agata'], [0, 1, 2, 3, 4])
        self.assertEqual(result['a0'], 1)
        self.assertEqual(result['a1'], 1)
        self.assertEqual(result['a2'], 1)
        self.assertEqual(result['g0'], 1)
        self.assertEqual(result['t0'], 1)

    def test_lscores_full_inclusions_two_words(self):
        result = get_letter_scores(['words', 'grama'], [0, 1, 2, 3, 4])
        self.assertEqual(result['w0'], 1)
        self.assertEqual(result['r0'], 2)
        self.assertEqual(result['a0'], 1)
        self.assertEqual(result['a1'], 1)

    def test_lscores_partial_inclusions(self):
        result = get_letter_scores(['agata'], [0, 1, 2, 3])
        self.assertEqual(result['a0'], 1)
        self.assertEqual(result['a1'], 1)
        self.assertFalse('a2' in result)

    def test_wscore_full_inclusions(self):
        word = 'krata'
        inclusions = range(WORD_SIZE)
        lscores = get_letter_scores([word], inclusions)
        self.assertEqual(get_word_score(word, inclusions, lscores), WORD_SIZE)

    def test_wscore_partial_inclusions(self):
        word = 'krata'
        inclusions = range(1, WORD_SIZE)
        lscores = get_letter_scores([word], inclusions)
        self.assertEqual(get_word_score(word, inclusions, lscores), WORD_SIZE - 1)

    def test_moves_ok_in_simple_case(self):
        self.assertEqual(next_move(['steki', 'stary', 'tarta'], []), 'stary')

    def test_solved_okeys_complete_state(self):
        self.assertTrue(solved([(0, 'k', GREEN), (1, 'r', GREEN), (2, 'a', GREEN), (3, 't', GREEN), (4, 'a', GREEN)]))

    def test_solved_fails_incomplete_state(self):
        self.assertFalse(solved([(0, 'k', GREEN), (1, 'r', GREEN), (2, 'a', GREEN), (3, 't', GREEN)]))

    def test_solved_fails_incomplete_state_with_yellow(self):
        self.assertFalse(solved([(0, 'k', GREEN), (1, 'r', GREEN), (2, 'a', GREEN), (3, 't', GREEN), (4, 'a', YELLOW)]))

if __name__ == '__main__':
    unittest.main()
