# -*- coding: utf-8 -*-

"""
Unique Candidate Technique.
Rather than looking at each cell like in the sole candidate technique,
we look at the grid by line/square/column. If there is a unique number in
the given possibilities of a square, then this number is right.
"""

from copy import deepcopy
from f_base import line, column, square


def make_list_uc(poss, c_list):
    a = [[0, (0, 0)] for i in range(10)]
    for i, j in c_list:
        if type(poss[i][j]) is list:
            for b in poss[i][j]:
                a[b][0] += 1
                a[b][1] = (i, j)
    return a


def unique_candidate(s, poss):
    """
    If there is only one number in one section (line/column/square) in the possibilities, then it chooses that number.
    :param s: sudoku
    :param poss: output of possibilities function
    :return: sudoku
    """
    sudoku = deepcopy(s)
    # For each square
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            occurences = make_list_uc(poss, square(i, j))
            for index, a in enumerate(occurences):
                if a[0] == 1:
                    x, y = a[1]
                    sudoku[x][y] = index

    # For each line
    for i in range(9):
        occurences = make_list_uc(poss, line(i, 0))
        for index, a in enumerate(occurences):
            if a[0] == 1:
                x, y = a[1]
                sudoku[x][y] = index

    # For each column
    for j in range(9):
        occurences = make_list_uc(poss, column(0, j))
        for index, a in enumerate(occurences):
            if a[0] == 1:
                x, y = a[1]
                sudoku[x][y] = index
    return sudoku
