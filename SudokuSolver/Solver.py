from f_base import won, check, P, possibilities, format_sudoku
from f_solcan import sole_candidate
from f_naksub import naked_subset
from f_unican import unique_candidate
from copy import deepcopy

sudoku = '900700500000910000640000900570040230000103000064080079009000024000098000008001007'

sudoku = format_sudoku(sudoku)
print(check(sudoku))

while 'before != sudoku':

    before = deepcopy(sudoku)
    poss = possibilities(sudoku)
    poss = naked_subset(poss)
    sudoku = sole_candidate(sudoku, poss)
    sudoku = unique_candidate(sudoku, poss)

    if before == sudoku:
        break

P(sudoku)