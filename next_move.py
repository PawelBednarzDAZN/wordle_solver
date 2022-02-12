# -*- coding: iso-8859-2 -*-
from consts import WORD_SIZE, GREEN, YELLOW, GREY, RED, NO_POSITION
from collections import defaultdict

# we assume non-nonsense states only - no validation on state length, position repetitions etc for performance sake
def matches_state(word, state):
    partials = []
    no_greens = list(word)
    # greens in positions
    for (position, letter, color) in filter(lambda (_1, _2, c): c == GREEN, state):
        if word[position] != letter:
            return False
    for (position, letter, color) in filter(lambda (_1, _2, c): c == YELLOW, state):
        if not letter in ''.join(word[:position] + word[position + 1:]):
            return False
    for (position, letter, color) in filter(lambda (_1, _2, c): c == GREY, state):
        if letter in word:
            return False
    for (position, letter, color) in filter(lambda (_, l, c): c == RED, state):
        if word.count(letter) < 2:
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

def solved(state):
    return set(range(WORD_SIZE)) == set([p for (p, _, c) in state if c == GREEN])

def extend_state(old_state, new_elements, last_word):
    state = old_state + new_elements
    for (p1, l1, c1) in new_elements:
        for (p2, l2, c2) in new_elements:
            if (p1, l1, c1) != (p2, l2, c2) and c1 == c2 == YELLOW and l1 == l2 and p1 != p2:
                state.append((NO_POSITION, l1, RED))
    to_grey_out = set(last_word) - set(map(lambda (p, l, c): l, state))
    state = state + map(lambda l: (NO_POSITION, l, GREY), to_grey_out)
    return list(set(state))

def next_move(words, state):
    words = filter(lambda word: matches_state(word, state), words)
    if len(words) == 0:
        print('No words in db satisfy these criteria')
        return ''
    inclusions = get_inclusions(state)
    letter_scores = get_letter_scores(words, inclusions)
    word_scores = [(word, get_word_score(word, inclusions, letter_scores)) for word in words]
    return max(word_scores, key = lambda (w, s): s)[0]

