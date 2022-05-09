# -*- coding: utf-8 -*-
#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *
from GUI.drawGame import *
from GUI.events import *
import os
import math
import time
from tkinter import filedialog 
from tkinter import *
from tkinter import messagebox
from extract_grid import extract_grid
from valeurs import *
from functions import printS

#Taille de la fenêtre du jeu
window_H = 600
window_W = 900    


def main():
    #Initialisation de la bibliothèque Pygame
    pygame.init()
    pygame.mixer.music.load("GUI/fondmusic.wav")

    
    on = True
    choice = False
    
    #P0 représente le point le plus à gauche et en haut de la grille
    P0 = (110,330)

    mode = 0; #0 mode sans aide, 1 chiffre bon -> vert, 2 chiffre non autorisé -> rouge

    #Création de la fenêtre
    screen = pygame.display.set_mode((window_H, window_W),RESIZABLE)

    #Boucle
    current_highlighted = None # représente si elle existe une case sélectionnée sur l'interface graphique
    key_0 = 256
    key_erase = 8
    
    #Variable pour bloquer une case sélectionnée
    locked_case = False
    #Variable qui continue la boucle si = 1, stoppe si = 0
    continuer = 1

    while continuer:
        on = True
        choice = False
        #Affichage ecran d'accueil
        screen.blit(accueil,(0,0))
        screen.blit(importbutton,(100,375))
        screen.blit(bouton_son,(0,0))
        pygame.mixer.music.play()


        pygame.display.flip()

        continuer_jeu = 1
        continuer_accueil = 1

        while continuer_accueil:
            continuer_jeu = 1

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer_accueil = 0
                    continuer_jeu = 0
                    continuer = 0
                if event.type == QUIT:    
                    continuer = 0
                    continuer_accueil =0
                    continuer_jeu = 0    
                if event.type == KEYDOWN and event.key ==K_a and choice == True:
                    mode = 2
                    continuer_accueil = 0
                if event.type == KEYDOWN and event.key ==K_z and choice == True:
                    mode = 0
                    continuer_accueil = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # on récupère la position de la souris dans une variable mousepos
                    mousepos = pygame.mouse.get_pos()
                    
                    # Ouverture de la grille
                    if clicButton(mousepos,100,375,400,150) == True:
                        root = Tk()
                        root.filename = filedialog.askopenfilename(initialdir = "data/",title = "Select file",filetypes = (("all files","*.*"),("png files","*.png"),("jpeg files","*.jpg")))
                        print (root.filename)
                        
                        #chargement de la photo du jeu et des grilles associées
                        G_init, G_sol = extract_grid(root.filename)
                        G_temp = G_init
                        printS(G_init)
                        printS(G_temp)
                        printS(G_sol)

                        grid_image = pygame.image.load(img_grid)
                        root.destroy()
                        grid_image = pygame.transform.scale(grid_image,(400,400))
                        
                        #taille d'une case -> dépend du nombre de cases dans la grille -> à lier avec la partie computer vision
                        case_size = int(grid_image.get_height()//9)
                        if choice == False:
                            screen.blit(choice_window,P0)
                            pygame.display.flip()
                            choice = True
                    
                    if clicButton(mousepos,0,0,30,30) == True:
                        if on == True :
                            screen.blit(bouton_mute,(0,0))
                            pygame.display.flip()
                            pygame.mixer.music.stop()

                            print(on)
                            on = False
                        else:
                            print(on)
                            screen.blit(bouton_son,(0,0))
                            pygame.display.flip()
                            pygame.mixer.music.play()

                            on = True
        
        
        # initialiser GUI a faire qu'une fois 
        chronostart = False
        if on == True:
            pygame.mixer.music.play() #on lance la musique

        gridGUI = initGameGUI(P0, case_size, G_temp)
        drawGame(screen, gridGUI,grid_image, P0)
        pygame.display.flip()
        chrono = 0
                        
        while continuer_jeu:

            if G_sol == G_temp:
                screen.blit(jeu,(0,0))
                screen.blit(image_victoire,(20,500))
                pygame.display.flip()
                time.sleep(5)
                continuer_jeu = 0

            screen.blit(bouton_chrono,(20,45))
            #screen.blit(menu_button,(0,700))

            # GESTION CHRONO 
            if chronostart:
                time.sleep(1)
                chrono += 1 
                if (math.floor(chrono % 60) < 10) and (math.floor(chrono / 60) < 10) :
                    affichage_chrono = '0' + str(math.floor(chrono / 60)) + ' : 0' + str(chrono % 60)
                elif (math.floor(chrono / 60) < 10):
                    affichage_chrono = '0' +  str(math.floor(chrono / 60)) + ' : ' + str(chrono % 60)
                else:
                    affichage_chrono = str(math.floor(chrono / 60)) + ' : ' + str(chrono % 60)
                font = pygame.font.Font(None, 30)
                chrono_surface = font.render(str(affichage_chrono), 50, RED)
                
                screen.blit(fond_chrono,(47,47))
                screen.blit(chrono_surface,(50,50))
                pygame.display.flip()

            else:
                if chrono == 0:
                    affichage_chrono = '00 : 00'
                    
                font = pygame.font.Font(None, 30)
                chrono_surface = font.render(str(affichage_chrono), 50, RED)
                
                screen.blit(fond_chrono,(47,47))
                screen.blit(chrono_surface,(50,50))
                pygame.display.flip()
                 
            for event in pygame.event.get():#On parcours la liste de tous les événements reçus
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer_accueil = 0
                    continuer_jeu = 0
                    continuer = 0
                 
                if event.type == QUIT:     #Si un de ces événements est de type QUIT
                    continuer = 0
                    continuer_jeu = 0      #On arrête la boucle
                
                # Si on a clic souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # on récupère la position de la souris dans une variable mousepos
                    mousepos = pygame.mouse.get_pos()
                    print(locked_case)

                    if clicButton(mousepos,0,800,80,80):
                        continuer_jeu = 0

                    if clicButton(mousepos,0,700, 80,80):
                        indice(G_init,G_sol,gridGUI,G_temp,mode)

                    if clicButton(mousepos,20,45,23,23):
                        chronostart = not chronostart

                    if not locked_case:
                        # si une case était déjà sélectionnée -> on la désactive sur l'interface graphique
                        if current_highlighted != None:
                            unhighlight_case(current_highlighted,gridGUI)
                        #on renvoit, si elle existe, la case sélectionnée
                        current_highlighted = clicOnGrid(mousepos, gridGUI)
                        #si une nouvelle case a été sélectionnée
                        if current_highlighted != None:
                            # on l'active dans l'interface graphique
                            highlight_case(current_highlighted, gridGUI)
                        #on redessine le jeu
                        drawGame(screen, gridGUI,grid_image, P0)
                    
                        pygame.display.flip()

                #si on a une entrée clavier et qu'une case est sélectionnée
                if current_highlighted != None and event.type == pygame.KEYDOWN:
                #si l'entrée est un chiffre entre 1 et 9
                    if key_0+9>=event.key>=key_0+1 :
                        # on rentre le chiffre choisi dans la case sélectionné sur l'interface graphique
                        inputNumber(current_highlighted, str(event.key-256), gridGUI, G_temp, G_sol, mode)
                        #bloque la case en mode 2 si c'est un faux numéro
                        if gridGUI[current_highlighted]['Color_Txt'] == RED :
                            locked_case = True
                        else :
                            locked_case = False
                        # on met à jour la grille
                        addValue(G_temp,current_highlighted,event.key-256)
                
                    # si on une entrée clavier de type suppression
                    if event.key == key_erase :
                        # on efface le chiffre dans l'interface graphique
                        eraseNumber(current_highlighted, gridGUI)
                        locked_case = False
                        # on met à jour la grille
                        removeValue(G_temp,current_highlighted)

                    # on redessine le jeu
                    drawGame(screen, gridGUI,grid_image, P0)

                    pygame.display.flip()


if __name__ == "__main__":
    main()
