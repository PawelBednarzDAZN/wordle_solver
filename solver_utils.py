#!/usr/bin/python
# coding: utf-8

from consts import *

def solved(state):
    return len(filter(lambda (_1, _2, c): c == GREEN, state)) == WORD_SIZE

def extend_state(old_state, new_elements, last_word):
    state = old_state + new_elements
    for (p1, l1, c1) in new_elements:
        for (p2, l2, c2) in new_elements:
            if c1 == c2 == YELLOW and l1 == l2 and p1 != p2:
                state.append((NO_POSITION, l1, RED))
    to_grey_out = set(last_word) - set(map(lambda (p, l, c): l, state))
    state = state + map(lambda l: (NO_POSITION, l, GREY), to_grey_out)
    return list(set(state))

# only greens and yellows
def state_delta(solution, guessed_word, old_state):
    state_d = []
    for (i, letter) in enumerate(guessed_word):
        if solution[i] == letter and (i, letter, GREEN) not in old_state:
            state_d.append((i, letter, GREEN))
    greens = [p for (p, _1, c) in state_d + old_state if c == GREEN]
    for (i, letter) in enumerate(guessed_word):
        if i not in greens and solution.count(letter) > len(
          filter(lambda (p, l, c): l == letter and c == GREEN, old_state + state_d) +
          filter(lambda (p, l, c): l == letter and c == YELLOW, state_d)
        ) and (i, letter, YELLOW) not in old_state:
            state_d.append((i, letter, YELLOW))
    return state_d
