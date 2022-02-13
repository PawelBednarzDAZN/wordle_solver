#!/usr/bin/python
# coding: utf-8
from collections import defaultdict

from consts import *

def solved(state):
    return len(filter(lambda (_1, _2, c): c == GREEN, state)) == WORD_SIZE

# only constraints that we are sure are still valid
def extend_state(state, delta):
    missed_green_letters = [l for (p, l, c) in state if c == GREEN and (p, l, c) not in delta]
    for (p, l, c) in delta:
        if c == GREEN and (p, l, c) not in state:
            # new greens get added
            state.append((p, l, c))
            if (NO_POSITION, l, RED) not in state:
                # new green softens all matching yellows if no matching red present
                for (py, ly) in [(py, ly) for (py, ly, cy) in state if l == ly and cy == YELLOW]:
                    state.remove((py, ly, YELLOW))
                    if (py, ly, SOFT_YELLOW) not in state:
                        state.append((py, ly, SOFT_YELLOW))
            else:
                # new green cancels matching red if present
                state.remove((NO_POSITION, l, RED))
    for (p, l, c) in delta:
        if c == GREY and (NO_POSITION, l, GREY) not in state:
            # new greys we can just add
            state.append((NO_POSITION, l, GREY))
        elif c == RED:
            if l not in missed_green_letters and (NO_POSITION, l, RED) not in state:
                state.append((NO_POSITION, l, RED))
        elif c == YELLOW:
            if missed_green_letters.count(l) == 0 or (missed_green_letters.count(l) == 1 and (NO_POSITION, l, RED) in delta):
                if (p, l, YELLOW) not in state:
                    state.append((p, l, YELLOW))
            elif (p, l, SOFT_YELLOW) not in state:
                state.append((p, l, SOFT_YELLOW))
    return state

# generate all the information gained from comparing the two words (completely disregarding previous knowledge)
def state_delta(solution, guessed_word):
    delta = []
    greens = defaultdict(int)
    for (i, letter) in enumerate(guessed_word):
        if solution[i] == letter:
            delta.append((i, letter, GREEN))
            greens[letter] += 1
    for (i, letter) in enumerate(guessed_word):
        if solution[i] != letter:
            if solution.count(letter) > greens[letter] + 1:
                delta.append((NO_POSITION, letter, RED))
            if solution.count(letter) > greens[letter]:
                delta.append((i, letter, YELLOW))
    for (i, letter) in enumerate(guessed_word):
        if (i, letter, GREEN) not in delta and (i, letter, YELLOW) not in delta:
            delta.append((NO_POSITION, letter, GREY))
    return delta
