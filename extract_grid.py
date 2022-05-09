import cv2
from functions import erase_create, image_resize, find_contours, find_square, warp_square, vignette, trieur, printS
from valeurs import *
from NumberRecognition.number_recognition import img_ML, predict
import numpy as np
import os, shutil
from PIL import Image
import torch


for name in [f_debug, f_cases, f_numbers]:
    erase_create(name)

def extract_grid(path):
    #### Extract Sudoku grid ####
    img = cv2.imread(path)
    # Resizing the image
    img = image_resize(img, height=800)

    c = find_contours(img, True, '')
    pts_img = find_square(c)

    h = img.shape[0]
    dst = warp_square(img, h, pts_img)

    cv2.imwrite(img_grid, dst)

    # Extract vignettes
    vignette(dst)

    # Sort them (empty versus filled with number)
    trieur()

    #### Number Recognition ####
    model = torch.load(f_model + 'model_font.pt', map_location=torch.device('cpu'))
    model.eval()

    # Create empty sudoku grid
    grid = [[0 for i in range(9)] for i in range(9)]

    list_folders = os.listdir(f_numbers)
    list_folders = [a for a in list_folders if '.png' in a]

    for p in list_folders:    
        img = Image.open(f_numbers + p)
        img.save(f_numbers + p)

        img_set = img_ML(f_numbers + p)

        nb, _ = predict(model, img_set)
        nb += 1
 
        grid[int(p[0])][int(p[1])] = int(nb)

    # Get grid
    printS(grid)

    #### Solveur ####
    from solveur import solveur
    grid_solved = solveur(grid)

    # Result
    printS(grid_solved)
    return grid, grid_solved

if __name__ == "__main__":
    a = extract_grid('data/grille9.jpg')
    print(a)