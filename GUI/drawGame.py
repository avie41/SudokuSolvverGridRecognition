# -*- coding: utf-8 -*-
#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *
from GUI.utilsGUI import *
from GUI.constantes import *

image_menu = pygame.image.load('GUI/menu.png')
image_menu = pygame.transform.scale(image_menu,(80,80))
image_victoire = pygame.image.load('GUI/victoire.gif')
image_victoire = pygame.transform.scale(image_victoire,(550,100))
ampoule = pygame.image.load('GUI/ampoule.png')
ampoule = pygame.transform.scale(ampoule,(80,80))
image_menu_rect = image_menu.get_rect()

accueil = pygame.image.load('GUI/fond_accueil.png')
choice_window = pygame.image.load('GUI/choice.jpg')
menu_button = pygame.image.load('GUI/menu.png')
menu_button = pygame.transform.scale(menu_button,(80,80))
importbutton = pygame.image.load('GUI/import.png')
bouton_son = pygame.image.load('GUI/bouton_son.png')
bouton_mute = pygame.image.load('GUI/bouton_mute.png')
fond_chrono = pygame.image.load('GUI/fond_chrono.png')
bouton_chrono =pygame.image.load('GUI/bouton_chrono.png')
bouton_chrono = pygame.transform.scale(bouton_chrono,(23,23))
fond_chrono = pygame.transform.scale(fond_chrono,(70,23))


def initGameGUI(P0, square_size, G):
    """
    fonction qui initialise la grille de l'interface du jeu
    Retourne une variable gridGUI = matrice de case à afficher
    Case = dictionnaire
    Paramètres d'entrée : P0 -> position en haut à gauche de la grille, 
    square_size -> taille d'une case, G-> grille de sudooku = matrice
    """
    gridGUI = {}
    for i in range(9) :
        for j in range(9) :
            position = (P0[0]+j*square_size,P0[1]+i*square_size)
            if G[i][j] == 0 :
                case = {'Value':None, 'Position': position, 'Size':square_size, 'Color_Txt': BLACK, 'Color_Case': TRANSPARENT}
                gridGUI[(i,j)] = case

    return gridGUI

jeu = pygame.image.load('GUI/fond_jeu.png')
def drawGame(screen, gridGUI, grid_image, P0):
    """
    fonction qui dessine le jeu
    """
    # Création d'une surface pour dessiner le jeu
    

    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    background = background.convert_alpha()
    background.blit(jeu,(0,0))
    
    # # Affichage du titre
    # font = pygame.font.Font(None, 36)
    # text = font.render("Sudoku", True, BLACK)
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # textpos.y = 10
    # background.blit(text, textpos)

    #Ajouter l'image de la grille
    background.blit(grid_image, P0)
    drawGrid(background, gridGUI)

    #"Blitter" dans le fenêtre
    screen.blit(background,(0,0))
    screen.blit(image_menu,(0,800))
    screen.blit(ampoule,(0,700))
    

def drawGrid(background, gridGUI):
    """
    fonction qui dessine la grille
    """
    # Principe : pour chaque case de la grille, on dessine la case
    for case in gridGUI :
        drawCase(background, gridGUI[case])


def drawCase(background, case):
    """
    fonction qui dessine une case de la grille
    """
    # on dessine un rectangle de la taille de la case et de la couleur de celle-ci
    if case['Color_Case'] != None :
        rect = pygame.Surface((case['Size']-4,case['Size']-4), pygame.SRCALPHA, 32)
        rect = rect.convert_alpha()
        rect.fill(case['Color_Case'])


    # si la case a une valeur, on ajoute ce texte dans la case
    if (case['Value'] != None):
        font_size = case['Size']
        font = pygame.font.Font(None, int(font_size))
        text = font.render(str(case['Value']), True, case['Color_Txt'])
        textpos = text.get_rect()
        textpos.centerx = rect.get_rect().centerx
        textpos.centery = rect.get_rect().centerx
        rect.blit(text, textpos)

    # on "blitte" la case dans le background
    background.blit(rect, (case['Position'][0]+2, case['Position'][1]+2))


'''def drawButton(background, text, posX, posY, sizeX, sizeY, color) :
    rect = pygame.Surface((sizeX, sizeY))
    rect.fill(color)
    font = pygame.font.Font(None, 24)
    text = font.render(text, True, WHITE)
    textpos = text.get_rect()
    textpos.centerx = rect.get_rect().centerx
    textpos.centery = rect.get_rect().centery
    rect.blit(text, textpos)
    background.blit(rect, (posX, posY))'''
