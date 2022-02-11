from consts import WORD_SIZE, GREEN, YELLOW
from collections import defaultdict

# we assume non-nonsense states only - no validation on state length, position repetitions etc for performance sake
def matches_state(word, state):
    partials = []
    no_greens = list(word)
    # greens in positions
    for (position, letter, color) in filter(lambda (_1, _2, c): c == GREEN, state):
        if word[position] != letter:
            return False
        else:
            no_greens[position] = 'G'
    for (position, letter, color) in filter(lambda (_1, _2, c): c == YELLOW, state):
        if not letter in ''.join(no_greens[:position] + no_greens[position + 1:]):
            return False
    return True

def get_inclusions(state):
    exclusions = [p for (p, l, c) in state if c == GREEN]
    return [i for i in range(WORD_SIZE) if (i not in exclusions)]

def get_scoring_keys(word, inclusions):
    scoring_keys = []
    incl_word = [word[i] for i in inclusions]
    for l in set(incl_word):
        for i in range(incl_word.count(l)):
            scoring_keys.append(l + str(i))
    return scoring_keys

# we assume all words match; state used only to discard 'green' positions
def get_letter_scores(words, inclusions):
    scores = defaultdict(int)
    for word in words:
        scoring_keys = get_scoring_keys(word, inclusions)
        for key in scoring_keys:
            scores[key] += 1
    return scores

# we assume scores were generated using the same inclusions and the word
def get_word_score(word, inclusions, scores):
    return sum([scores[key] for key in get_scoring_keys(word, inclusions)])

def next_move(words, state):
    inclusions = get_inclusions(state)
    letter_scores = get_letter_scores(words, inclusions)
    word_scores = [(word, get_word_score(word, inclusions, letter_scores)) for word in words]
    return max(word_scores, key = lambda (w, s): s)[0]

