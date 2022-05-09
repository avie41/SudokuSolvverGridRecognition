import pygame
from pygame.locals import *
from GUI.constantes import *
from GUI.drawGame import *
from GUI.utilsSudoku import *
from random import *

# fonction qui renvoit si elle existe la case de la grille sur laquelle l'utilisateur a cliqué
def clicOnGrid(mousepos, gridGUI):
    # principe : on parcourt toutes les cases de grille de l'interface
    # si il y a collision entre le rectangle de la case et la position de la souris
    # attention : il faut redéfinir ce rectangle !!!!
    # on renvoie la case en question
    # sinon on renvoie None
    for case in gridGUI:
        rect = pygame.Rect(gridGUI[case]['Position'][0], gridGUI[case]['Position'][1], gridGUI[case]['Size'], gridGUI[case]['Size'])
        if rect.collidepoint(mousepos):
            return case
    return None
def clicButton(mousepos,x,y,sizex,sizey):
    rect = pygame.Rect(x,y,sizex,sizey)
    if rect.collidepoint(mousepos):
            return True
    return False

# fonction qui active (ie change la couleur) d'une case
def highlight_case(coordinates, gridGUI):
    gridGUI[coordinates]['Color_Case'] = BLUE

# fonction qui désactive (ie change la couleur) d'une case
def unhighlight_case(coordinates, gridGUI):
    gridGUI[coordinates]['Color_Case'] = TRANSPARENT

# fonction qui initie la valeur d'une case
def inputNumber(coordinates, number, gridGUI, G, G_sol, mode):
    gridGUI[coordinates]['Value'] = int(number)
    updateColorCase(coordinates, gridGUI, G, G_sol, mode)

# fonction qui initie la valeur d'une case à None
def eraseNumber(coordinates, gridGUI):
    gridGUI[coordinates]['Value'] = None

# fonction qui ajoute une nouvelle valeur dans le jeu Sudoko
def addValue(G,coordinates,value) :
    G[coordinates[0]][coordinates[1]] = value

# fonction qui supprime une valeur dans le jeu Sudoku
def removeValue(G,coordinates) :
    G[coordinates[0]][coordinates[1]] = 0

# fonction qui met à jour la couleur
def updateColorCase(coordinates, gridGUI, G, G_sol, mode) :
    gridGUI[coordinates]['Color_Txt'] = BLACK
    if (mode==1) :
        if gridGUI[coordinates]['Value'] == G_sol[coordinates[0]][coordinates[1]] :
            gridGUI[coordinates]['Color_Txt'] = GREEN
    if (mode==2) : 
        if not is_authorized(gridGUI[coordinates]['Value'], coordinates,G) :
            gridGUI[coordinates]['Color_Txt'] = RED

def indice(G_init,G_sol,gridGUI,G_temp,mode):
    tabi=[]
    tabj=[]
    for i in range(9):
        for j in range(9):
            if(G_init[i][j]==0):
                if(gridGUI[(i,j)]['Value']==None):
                    tabi.append(i)
                    tabj.append(j)
    if len(tabi) != 0:
        theone=randint(0,len(tabi)-1)
        thei=tabi[theone]
        thej=tabj[theone]
        inputNumber((thei,thej), int(G_sol[thei][thej]), gridGUI, G_temp, G_sol, mode)
        addValue(G_temp,(thei,thej),int(G_sol[thei][thej]))
