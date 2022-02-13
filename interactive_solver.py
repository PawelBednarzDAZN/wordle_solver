# coding: utf-8
from slf_heuristic import next_move
from solver_utils import extend_state, solved
from consts import ROUNDS
from db import fetch

words = fetch('db/pl_pl.txt')
is_solved = False
round = 0
state = []
while not is_solved and round < ROUNDS:
    suggestion, words = next_move(words, state)
    if suggestion == '':
        break
    print("I suggest you go for " + suggestion)
    state = extend_state(state, input('Introduce the new info gained after the last move (except grayed-out letters). Previous info: ' + str(state) + ': '), suggestion)
    is_solved = solved(state)
    round += 1
