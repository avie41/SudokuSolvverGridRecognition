from os import system
from typing import *

Line = TypeVar('int')
Column = TypeVar('int')
Coordinate = TypeVar('Tuple[Line, Column]')
Value = TypeVar('int') # only {1, 2, 3, 4, 5}
Shape = TypeVar('int')
Tectonic = TypeVar('Tuple[Dict[Coordinate, Shape], Dict[Coordinate, Value]]')
Proposition = TypeVar('Tuple[bool, Line, Column, Value]')
Clause = TypeVar('List[Proposition]')
Constraint = TypeVar('List[Clause]')

# Quelques fonctions d'accès à la grille

def Lines (G: Tectonic) -> int:
    return len(G[0])

def Columns (G: Tectonic) -> int:
    return len(G[0][0])

def Coordinates (G: Tectonic) -> List[Coordinate]:
    """
    Returns the coordinates of the grid, by line in major and column in minor.
    """
    return [ (i, j)
             for i in range(1, Lines(G)   + 1)
             for j in range(1, Columns(G) + 1) ]

def Neighbours (G: Tectonic,
                i: Line,
                j: Column) -> List[Coordinate]:
    """
    Returns the coordinates of all the immediate neighbours of a cell coordinate.
    """
    assert 1 <= i <= Lines(G)
    assert 1 <= j <= Columns(G)
    return [ (i + d_i, j + d_j)
             for d_i in [-1, 0, 1]
             for d_j in [-1, 0, 1]
             if (d_i, d_j) != (0, 0)
             if 1 <= i + d_i <= Lines(G)
             if 1 <= j + d_j <= Columns(G) ]

def Shape (G: Tectonic,
           i: Line,
           j: Column) -> Shape:
    assert 1 <= i <= Lines(G)
    assert 1 <= j <= Columns(G)
    (C, _) = G
    return C[i - 1][j - 1]

def Shapes (G: Tectonic) -> Dict[Shape, List[Coordinate]]:
    S = { Shape(G, i, j)
          for (i, j) in Coordinates(G) }
    return { s: [ (i, j)
                  for (i, j) in Coordinates(G)
                  if Shape(G, i, j) == s ]
             for s in S }

def ShapeCells (G: Tectonic,
                ij: Coordinate) -> List[Coordinate]:
    """
    Returns the coordinates of all the cells belonging to the shape associated to the cell (i, j).
    """
    (i, j) = ij
    assert 1 <= i <= Lines(G)
    assert 1 <= j <= Columns(G)
    s = Shape(G, i, j)
    return [ (i, j)
             for (i, j) in Coordinates(G)
             if Shape(G, i, j) == s ] # les cases associées à la forme s

def ShapeValues (G: Tectonic,
                 ij: Coordinate) -> List[Value]:
    """
    Returns the authorised values in a the shape associated to the cell (i, j).
    They are necessarily a prefix set of {1, ..., 5}.
    """
    return range(1, len(ShapeCells(G, ij)) + 1)
    
def Show (G: Optional[Tectonic]):
    """
    Displays a tectonic game grid in text mode.
    """

    def FormatCell (G: Tectonic,
                    ij: Coordinate) -> str:
        (_, V) = G
        return " {0} ".format(V[ij]) if ij in V else " . "

    def FormatLineCells (G: Tectonic,
                         i: Line) -> List[str]:
        return [ FormatCell(G, (i, j))
                 for j in range(1, Columns(G) + 1) ]

    def FormatVerticalDelimiters (G: Tectonic,
                                  i: Line) -> List[str]:
        return ["|"] + [ " " if Shape(G, i, j) == Shape(G, i, j-1) else "|"
                         for j in range(2, Columns(G) + 1) ] + ["|"]
        
    def FormatLine (G: Tectonic,
                    i: Line) -> str:
        cs = FormatLineCells(G, i)
        ds = FormatVerticalDelimiters(G, i)
        assert len(cs) + 1 == len(ds)
        return ds[0] + "".join([ c + d
                                 for (c, d) in zip(cs, ds[1:]) ])

    def Intersection (h: bool,
                      v: bool) -> str:
        """
        Character to be used at the intersection of four cells depending on the fact that values belong to the same shape horizontally and/or vertically.
        """
        return { (True,  True ): " ",
                 (False, True ): "|",
                 (True,  False): "-",
                 (False, False): "+" }[(h, v)]
    
    def FormatIntersectionDelimiters (G: Tectonic,
                                      i: Line) -> List[str]:
        assert 1 <= i < Lines(G)
        return [ Intersection(False,
                              Shape(G, i, 1) == Shape(G, i+1, 1)) ] + \
               [ Intersection(Shape(G, i, j-1) == Shape(G, i,   j  ) and Shape(G, i+1, j-1) == Shape(G, i+1, j),
                              Shape(G, i, j-1) == Shape(G, i+1, j-1) and Shape(G, i,   j  ) == Shape(G, i+1, j))
                 for j in range(2, Columns(G) + 1) ] + \
               [ Intersection(False,
                              Shape(G, i, Columns(G)) == Shape(G, i+1, Columns(G))) ]
        
    def FormatHorizontalDelimiters (G: Tectonic,
                                    i: Line) -> List[str]:
        assert 1 <= i < Lines(G)
        return [ "   " if Shape(G, i, j) == Shape(G, i+1, j) else "---"
                 for j in range(1, Columns(G) + 1) ]
    
    def FormatIntersectionLine (G: Tectonic,
                                i: Line) -> str:
        assert 1 <= i < Lines(G)
        hs = FormatHorizontalDelimiters(G, i)
        ds = FormatIntersectionDelimiters(G, i)
        assert len(hs) + 1 == len(ds)
        return ds[0] + "".join([ h + d
                                 for (h, d) in zip(hs, ds[1:]) ])
    
    def FormatFirstIntersectionLine (G: Tectonic) -> str:
        return "+---" + "".join([ Intersection(Shape(G, 1, j-1) == Shape(G, 1, j),
                                               False) + "---"
                                  for j in range(2, Columns(G) + 1) ]) + "+"
    
    def FormatLastIntersectionLine (G: Tectonic) -> str:
        i = Lines(G)
        return "+---" + "".join([ Intersection(Shape(G, i, j-1) == Shape(G, i, j),
                                               False) + "---"
                                  for j in range(2, Columns(G) + 1) ]) + "+"
    
    if G == None:
        print("No grid")
    else:
        assert len(Coordinates(G)) == Lines(G) * Columns(G), "Missing coordinates in the game"
        (C, V) = G
        print(FormatFirstIntersectionLine(G))
        for i in range(1, Lines(G)):
            print(FormatLine(G, i))
            print(FormatIntersectionLine(G, i))
        print(FormatLine(G, Lines(G)))
        print(FormatLastIntersectionLine(G))

# Dérivation des contraintes du jeu

def ValueConstraints (G: Tectonic) -> Constraint:
    return [ [ (True, i, j, k)
               for k in ShapeValues(G, (i, j)) ]
             for (i, j) in Coordinates(G) ]
    
def UnicityConstraints (G: Tectonic) -> Constraint:
    return [ [ (False, i, j, k), (False, i, j, m) ]
             for (i, j) in Coordinates(G)
             for k in ShapeValues(G, (i, j))
             for m in ShapeValues(G, (i, j))
             if k < m ]

def EnumerationConstraints (G: Tectonic) -> Constraint:
    S = Shapes(G)
    return [ [ (False, i, j, k), (False, a, b, k) ]
             for s in S
             for (i, j) in S[s]
             for (a, b) in S[s]
             if (i, j) < (a, b)
             for k in ShapeValues(G, (i, j))]

def NeighbouringConstraints (G: Tectonic) -> Constraint:
    return [ [ (False, i, j, k), (False, a, b, k) ]
             for (i, j) in Coordinates(G)
             for k in ShapeValues(G, (i, j))
             for (a, b) in Neighbours(G, i, j) ]

def PresetConstraints (G: Tectonic) -> Constraint:
    (_, V) = G
    return [ [ (True, i, j, V[(i, j)]) ]
             for (i, j) in V ]

def GameConstraints (G: Tectonic) -> Constraint:
    return ValueConstraints(G)        + \
           UnicityConstraints(G)      + \
           EnumerationConstraints(G)  + \
           NeighbouringConstraints(G) + \
           PresetConstraints(G)

# Traduction vers et depuis le format Dimacs

def VariablesNumber (G: Tectonic) -> int:
    """
    Returns the number of Boolean variables necessary to represent a Tectonic game.
    """
    return Lines(G) * Columns(G) * 5

def ijk2v (G: Tectonic,
           i: Line,
           j: Column,
           k: Value) -> int:
    """
    Associates a given Tectonic coordinate and value to a single Boolean value (as in index).
    
    Cells are numbered from left to right (column by column), then from top to bottom (line by line), finally by plane.
    
    (1, 1, 1) is associated to 1.
    """
    assert 1 <= i <= Lines(G)
    assert 1 <= j <= Columns(G)
    assert 1 <= k <= 5
    return 1                               + \
           (j - 1)                         + \
           (i - 1) *            Columns(G) + \
           (k - 1) * Lines(G) * Columns(G)

def v2ijk (G: Tectonic,
           v: int) -> Tuple[Line, Column, Value]:
    """
    Reverses ijk2v.
    """
    assert 1 <= v <= Lines(G) * Columns(G) * 5
    (k, m) = divmod(v - 1, Lines(G) * Columns(G))
    (i, j) = divmod(m    ,            Columns(G))
    return (i + 1, j + 1, k + 1)


def nijk2v (G: Tectonic,
            n: bool,
            i: Line,
            j: Column,
            k: Value) -> int:
    """
    Associates a propositional literal to a *signed* Boolean index.
    """
    assert 1 <= i <= Lines(G)
    assert 1 <= j <= Columns(G)
    assert 1 <= k <= 5
    return ijk2v(G, i, j, k) if n else - ijk2v(G, i, j, k)

def prop_v2ijk2_ijk2v_id (G: Tectonic):
    return all([ v2ijk(G, ijk2v(G, i, j, k)) == (i, j, k)
                 for (i, j) in Coordinates(G)
                 for k in ShapeValues(G, (i, j)) ])

def DimacsConstraints (G: Tectonic) -> List[List[int]]:
    return [ [ nijk2v(G, n, i, j, k)
               for (n, i, j, k) in Cs ]
             for Cs in GameConstraints(G) ]

def ShowConstraints (G: Tectonic):
    Cs = DimacsConstraints(n, G)
    print("p cnf " + str(n**6) + " " + str(len(Cs)))
    for C in Cs:
        print(" ".join([ str(p)
                         for p in C ]) + " 0")

# Résolution du jeu

def WriteDimacsFile (G: Tectonic):
    with open("tectonic.cnf", "w") as f:
        Cs = DimacsConstraints(G)
        f.write("p cnf " + str(VariablesNumber(G)) + " " + str(len(Cs)) + "\n")
        for C in Cs:
            f.write(" ".join([ str(p)
                               for p in C ]) + " 0\n")

def ReadDimacsSolution ():
    with open("tectonic_solution.cnf", "r") as f:
        c = f.read()
    r = c.split()
    if r[0] == "UNSAT":
        return None
    else:
        return [ int(p)
                 for p in r[1:] ]

def Solve (G: Tectonic) -> Tectonic:
    WriteDimacsFile(G)
    system("minisat tectonic.cnf tectonic_solution.cnf")
    r = ReadDimacsSolution()    
    if r == None:
        return None
    else:
        s = [ v2ijk(G, v)
              for v in r
              if v > 0 ]
        assert len(s) == Lines(G) * Columns(G) # all cells assigned
        (C, V) = G
        V2 = { (i, j): k
               for (i, j, k) in s }
        assert all([ V[(i, j)] == k
                     for (i, j, k) in s
                     if (i, j) in V ]) # pre-assigned cells unchanged
        return (C, V2)

# Des grilles à résoudre

G1 = ([ [1, 1, 2], # solution unique (élémentaire pour minisat)
        [1, 3, 2],
        [3, 3, 3] ], # grille avec affectation de chaque cellule à sa forme
      {}) # aucune valeur pré-positionnée

G2 = ([ [1, 1, 2, 2, 2], # facile
        [1, 1, 2, 2, 3],
        [1, 4, 5, 6, 6],
        [4, 4, 6, 6, 6],
        [4, 4, 7, 7, 7],
        [8, 8, 8, 7, 7],
        [8, 8, 9, 9, 9] ], # grille avec affectation de chaque cellule à sa forme
      {(1, 1): 5, (1, 5): 3,
       (2, 2): 3, (2, 3): 5,
       (3, 4): 3,
       (4, 3): 2, (4, 4): 5,
       (6, 2): 5, (6, 3): 2, (6, 5): 4,
       (7, 1): 3, (7, 4): 3}) # valeurs pré-positionnées

G3 = ([ [1, 1, 2, 3, 3],  # soit disant intermédiaire (le plus facile pour minisat !)
        [1, 2, 2, 3, 3],
        [4, 4, 2, 5, 3],
        [4, 4, 2, 5, 5],
        [4, 6, 6, 5, 5],
        [6, 6, 7, 7, 7],
        [6, 8, 8, 8, 8] ], # grille avec affectation de chaque cellule à sa forme
      {(1, 4): 2,
       (2, 4): 5,
       (3, 1): 3,
       (4, 1): 4,
       (5, 2): 1, (5, 3): 3,
       (6, 2): 4}) # valeurs pré-positionnées

G4 = ([ [1, 1, 1, 2, 2], # soit disant difficile (plus facile pour minisat !)
        [1, 1, 3, 2, 2],
        [4, 3, 3, 3, 2],
        [5, 5, 6, 6, 6],
        [5, 5, 7, 6, 6],
        [5, 7, 7, 8, 8],
        [7, 7, 8, 8, 8] ], # grille avec affectation de chaque cellule à sa forme
      {(1, 1): 3, (1, 4): 1,
       (2, 2): 2, (2, 4): 3,
       (3, 5): 4,
       (5, 1): 4, (5, 5): 2,
       (6, 5): 1,
       (7, 1): 1}) # valeurs pré-positionnées

G5 = ([ [1, 1, 1, 2, 2], # enfin "difficile" pour minisat !
        [1, 1, 3, 2, 2],
        [4, 3, 3, 3, 2],
        [5, 5, 6, 6, 6],
        [5, 5, 7, 6, 6],
        [5, 7, 7, 8, 8],
        [7, 7, 8, 8, 8] ], # grille avec affectation de chaque cellule à sa forme
      {}) # c'est-à-dire G4 sans valeurs pré-positionnées

G6 = ([ [1, 1, 1, 2,  2,  9, 10, 12, 12], # sans solution !
        [1, 1, 3, 2,  2,  9, 10, 10, 12],
        [3, 3, 3, 3,  9,  9,  9, 10, 12],
        [5, 5, 6, 6,  6, 11, 15, 15, 12],
        [5, 5, 7, 6,  6, 11, 15, 15, 16],
        [5, 7, 7, 8, 11, 11, 14, 15, 14],
        [7, 7, 8, 8,  8, 11, 14, 14, 14] ],
      {})

G7 = ([ [1, 1, 1, 2, 2],
        [3, 1, 1, 2, 2],
        [3, 4, 4, 5, 5],
        [3, 4, 4, 5, 5],
        [3, 6, 4, 7, 5] ],
      {(1, 2): 4, (1, 5): 3,
       (2, 5): 4,
       (4, 3): 5, (4, 5): 5})

G8 = ([ [  1,  1,  1,  1,  2,  2,  2 ],
        [  3,  4,  5,  1,  2,  2,  6 ],
        [  3,  4,  5,  7,  7,  7,  6 ],
        [  4,  4,  9,  8,  7,  6,  6 ],
        [  4,  9,  9,  9, 11, 11,  6 ],
        [ 10, 10,  9, 11, 11, 11, 12 ],
        [ 10, 10, 14, 13, 13, 12, 12 ],
        [ 10, 14, 14, 16, 13, 13, 13 ],
        [ 15, 14, 14, 16, 16, 16, 16 ]  ],
      {})

