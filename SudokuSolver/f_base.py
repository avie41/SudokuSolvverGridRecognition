# -*- coding: utf-8 -*-

"""
Base functions used in the different solving techniques.
"""

import numpy as np
from copy import deepcopy


def format_sudoku(s):
    out = []
    for i in range(0, 81, 9):
        out.append(list(s[i:i+9]))

    out = np.array(out)
    out = out.astype(int)

    return out.tolist()


def line(i, _):
    return [(i, a) for a in range(9)]


def column(_, j):
    return [(a, j) for a in range(9)]


def square(i, j):
    m, n = i//3, j//3
    return [(a, b) for a in range(m*3, m*3+3) for b in range(n*3, n*3+3)]


def gen():
    for i in range(9):
        for j in range(9):
            yield i, j


def check(s):
    """
    Checks whether the sudoku presents mistakes or not.
    It doesn't need to be full to be tested.
    :param s: sudoku to be tested
    :return: True if the sudoku is ok, False if a mistake has been made solving the sudoku
    """
    d = True
    for i, j in gen():
        nb_line = [s[x][y] for x, y in line(i, j) if s[x][y] != 0]
        nb_col = [s[x][y] for x, y in column(i, j) if s[x][y] != 0]
        nb_sq = [s[x][y] for x, y in square(i, j) if s[x][y] != 0]
        for a, b, c in zip(nb_line, nb_col, nb_sq):
            if nb_line.count(a) != 1 or nb_col.count(b) != 1 or nb_sq.count(c) != 1:
                d = False
                print('Problem on cell ({}, {})'.format(i, j))
                break
    return d


def possibilities(s):
    """
    Stores in the poss array the possibles numbers for each empty cell.
    :param s: sudoku
    :return: poss array
    """
    poss = deepcopy(s)

    for i in range(9):
        for j in range(9):
            if s[i][j] == 0:
                a = set()

                for x, y in line(i, j) + square(i, j) + column(i, j):
                    a.add(s[x][y])

                b = {a for a in range(1, 10)}
                poss[i][j] = list(b - a)

    return poss


def P(s):
    """
    Prints the sudoku as a square, so it is easily readable
    :param s: sudoku
    :return: nothing
    """
    p = deepcopy(s)
    p = np.array(p)
    p = p.astype(str)
    p = p.tolist()

    print('\n'.join(['  '.join(a) for a in p]))
    print('\n')


def won(s):
    w = True
    for l in s:
        if 0 in l:
            w = False
    return w
