#!/usr/bin/python
# -*- coding: iso-8859-2 -*-
from next_move import next_move, extend_state, solved
from consts import ROUNDS

db = map(lambda s: s.strip(), open('db/pl_pl.txt').readlines())

is_solved = False
round = 0
state = []
while not is_solved and round < ROUNDS:
    suggestion = next_move(db, state)
    if suggestion == '':
        break
    print("I suggest you go for " + suggestion)
    state = extend_state(state, input('Introduce the new info gained after the last move (except grayed-out letters). Previous info: ' + str(state) + ': '), suggestion)
    is_solved = solved(state)
    round += 1
