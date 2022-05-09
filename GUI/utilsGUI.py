# -*- coding: utf-8 -*-
#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *

from os import system
from typing import *

Position = TypeVar('Tuple[int,int]')
Taille = TypeVar('int')
Couleur = TypeVar('Tuple[int,int,int,int]')
CaseGUI = TypeVar('Dict[str,]') # clés = (valeur,position,taille,couleur_txt,couleur_fond)
GridGUI = TypeVar('Dict[Coordinate,CaseGUI]')

