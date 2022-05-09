import os

def calcul_de_c(a):
    l, c, couche = a
    l -= 1
    couche -= 1
    return l*9 + c +81*couche 


def nba(h):
    couche = (h-1) // 81
    h = h - couche*81
    l = (h-1) // 9
    c = h - l * 9

    l += 1
    couche += 1
    return l, c, couche


def solveur(T):
    clauses = 0
    with open('sudoku.cnf', 'w') as f:
        f.write('\n')

        # numbers already in grid
        nb = [calcul_de_c((i+1, j+1, T[i][j])) for i in range(9) for j in range(9) if T[i][j] != 0]
        for i in nb:
            f.write(str(i) + ' 0\n')
            clauses += 1

        # lines
        lines = [ [j for j in range(i+1, i+10)] for i in range(0,81*9,9) ]
        columns = [ [a*81 + j + i*9 for i in range(9)] for a in range(9) for j in range(1,10,1)]
        # square 
        squares = [ [j, j + 1,j + 2] for j in range(1,9*81,9)] + [ [j, j + 1, j + 2] for j in range(4,9*81,9)] + [ [j, j + 1, j + 2] for j in range(7,9*81,9)]
        print(squares[0])
        squares = [squares[x]+squares[x+1]+squares[x+2] for x in range(0,len(squares),3)]

        # line through the "couches"
        lines_c = [ [i+j*81 for j in range(9)] for i in range(1, 82) ]

        test = lines + columns + squares + lines_c
        bug=0
        
        for a in test:
            # at least a 1
            f.write(' '.join([str(x) for x in a ]) + ' 0\n')
            clauses += 1
        
            # at most a 1
            bug+=1
            #print(bug)
            for i in range(9):
                for j in range(i+1, 9):
                    f.write('-' + str(a[i]) + ' -' + str(a[j]) +  ' 0\n')
                    clauses += 1

    # We add the number of clauses
    with open('sudoku.cnf', 'r') as file:
        data = file.readlines()

    # now change the 2nd line, note that you have to add a newline
    data[0] = 'p cnf ' + str(9**3) + ' ' + str(clauses) + '\n'

    with open('sudoku.cnf', 'w') as file:
        file.writelines(data)

    # MINISAT
    os.system('minisat sudoku.cnf sol.cnf')

    with open('sol.cnf', 'r') as f:
        t = f.read()

    import re
    t = re.findall(r'[+-]?\d+(?:\.\d+)?', t)
    t = [int(x) for x in t]
    t = [x for x in t if x > 0]

    A = [ [0 for i in range(9)] for j in range(9)]

    for i in t:
        l, c, cou = nba(i)
        A[l-1][c-1] = cou

    return A
