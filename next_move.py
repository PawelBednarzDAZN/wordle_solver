from consts import WORD_SIZE, GREEN, YELLOW

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
