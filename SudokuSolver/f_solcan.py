# -*- coding: utf-8 -*-

"""
Sole candidate technique.
If there is only one possibility in a cell, because
of the constraints of the other numbers, then it can only
be this number.
"""

from copy import deepcopy


def sole_candidate(s, poss):
    sudoku = deepcopy(s)
    for i in range(9):
        for j in range(9):
            a = poss[i][j]
            if type(a) is list:
                if len(a) == 1:
                    sudoku[i][j] = a[0]

    return sudoku
