# -*- coding: utf-8 -*-

"""
Unique Candidate Technique.
Rather than looking at each cell like in the sole candidate technique,
we look at the grid by line/square/column. If there is a unique number in
the given possibilities of a square, then this number is right.
"""

from copy import deepcopy
from f_base import line, column, square


def subset(poss, c_list):
    out = []
    # Get the numbers and possibilities for the comprehension list entered
    a = [poss[i][j] for i, j in c_list if type(poss[i][j]) is list]
    for nb_possible in a:
        if a.count(nb_possible) == len(nb_possible) and nb_possible not in out and len(nb_possible) > 1:
            out.append(nb_possible)

    return out


def sub_nb(p, c_list, nb):
    poss = deepcopy(p)

    for x, y in c_list:
        if type(poss[x][y]) is list and poss[x][y] != nb:
            poss[x][y] = list(set(poss[x][y]) - set(nb))

    return poss


def naked_subset(p):
    poss = deepcopy(p)

    # For each square
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # We spot any subset
            nb = subset(poss, square(i, j))
            # if len(nb) > 0:
            #     print(nb, i, j)
            # We remove the numbers in the subset from other positions
            for a in nb:
                poss = sub_nb(poss, square(i, j), a)

    # For each line
    for i in range(9):
        nb = subset(poss, line(i, 0))
        # if len(nb) > 0:
        #     print(nb, i, 0)
        # We remove the numbers in the subset from other positions
        for a in nb:
            poss = sub_nb(poss, line(i, 0), a)

    # For each column
    for j in range(9):
        nb = subset(poss, column(0, j))
        # if len(nb) > 0:
        #     print(nb, 0, j)
        # We remove the numbers in the subset from other positions
        for a in nb:
            poss = sub_nb(poss, column(0, j), a)

    return poss