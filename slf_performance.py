from slf_heuristic import next_move
from solver_utils import *
from db import fetch
from colors import magenta, color
from consts import LOADS

def measure_performance(db_file, output_file, test_set_size=LOADS, verbose=False, progress_steps=1):
    words = fetch(db_file)
    test_words = words[:test_set_size]
    rounds_required = []
    all = len(test_words)
    for (i, word) in enumerate(test_words):
        active_words = words
        is_solved = False
        round = 0
        state = []
        if verbose:
            print(magenta(word))
        while not is_solved:
            suggestion, active_words = next_move(active_words, state)
            if suggestion == '':
                print 'no word satisfied the conditions for', word
                round = 20
                break
            delta = state_delta(word, suggestion)
            state = extend_state(state, delta)
            if verbose:
                print color(suggestion, state)
            is_solved = solved(state)
            round += 1
            if round > 19:
                print 'infinite loop for', word
                break
        rounds_required.append(round)
        if progress_steps != 1 and i % (all / progress_steps) == 0:
            print '%.2f%% done' % ((float(i) / all) * 100)

    f = open(output_file, 'w')
    for (i, r) in enumerate(rounds_required):
        f.write(str(r) + ('\n' if i < len(rounds_required) - 1 else ''))
    f.close()
