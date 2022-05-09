***Attention, ce programme nécessite les modules suivants : PIL, torch, torchvision, pygame, tkinter, imutils, OpenCV, Numpy ainsi que MiniSat.***

# Reconnaissance et résolution d'une grille de Sudoku

_Ce projet vise à reconnaître sur une photo une grille de sudoku, à en extraire les nombres et à la résoudre. Une interface est également proposé pour permettre à un utilisateur de jouer sur la grille._

**Pour faire lancer le programme, il suffit de lancer le fichier GUI.py**

## Les fonctionnalités que nous avons ajoutées
* Un chronomètre sur l'interface
* Une musique de fond. Elle peut être ennuyante à force, c'est pourquoi nous avons également ajouté un bouton ON/OFF.
* Plusieurs niveaux d'aides. Une première aide qui colorie en rouge un chiffre qui ne peut pas être ici et une seconde qui affiche un chiffre supplémentaire au hasard.

## Les difficultés que nous avons eu

* La reconnaissance des chiffres. Le modèle entraîné sur la base de donnée MNIST n'atteignait que 80% de précision sur nos données. Nous avons donc entraîné d'autres modèles sur différentes bases de données que nous avons créés. Celle qui a fonctionnée le mieux a été une base de donnée remplie de chiffres générés à l'aide des polices proposées par Google. Nous avons ainsi atteint 93% de précision.

## Ce que nous n'avons pas eu le temps de faire.

* Nous aurions aimé ajouter un indice personalisé en faisant tourner le programme de résolution manuelle (dans le dossier `SudokuSolver`)
* Nous voulions aussi ajouté une coloration des cases en fonction de la case sélectionnée, pour que le jeu soit plus agréable.

## Installation des modules utilisés

`pip install Pillow numpy python-opencv torch torchvision pygame tkinter imutils`  
Pour Minisat, voir les instructions données sur le site du projet.