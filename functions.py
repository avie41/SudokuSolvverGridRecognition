# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os, shutil
from PIL import Image
from imutils import contours, convenience
from valeurs import *
from random import randint


def vignette(image):
    # Load image, grayscale, and adaptive threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 57, 5)
    cv2.imwrite(f_debug + 'vign_thresh.png', thresh)

    # Filter out all numbers and noise to isolate only boxes
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = adjust_contours(cnts)
    # Approximate area of a square
    area_square = (image.shape[0]/9)**2

    for c in cnts:
        area = cv2.contourArea(c)
        if area < area_square/3:
            cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

    cv2.imwrite(f_debug + 'vign_grid.png', thresh)
    # Fix horizontal and vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=9)

    cv2.imwrite(f_debug + 'vign_grid_better.png', thresh)
    # Sort by top to bottom and each row by left to right
    invert = 255 - thresh
    cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

    sudoku_rows = []
    row = []
    for (i, c) in enumerate(cnts, 1):
        area = cv2.contourArea(c)
        if area < 50000:
            row.append(c)
            if i % 9 == 0:  
                cnts = contours.sort_contours(row, method="left-to-right")
                cnts = adjust_contours(cnts)
                sudoku_rows.append(cnts)
                row = []

    # Iterate through each box
    j = 0
    for row in sudoku_rows:
        for c in row:
            # Getting the deformed square
            peri = cv2.arcLength(c, True)
            square = cv2.approxPolyDP(c, 0.04 * peri, True)
            square = np.array([list(i[0]) for i in square])
            pts_img = order_points(square)

            if len(pts_img) == 4:
                # Deforming the shape to a perfect square
                dst = warp_square(image, image.shape[0]/9, pts_img)
                # dst = cv2.resize(dst, (28, 28), interpolation = cv2.INTER_AREA) 
                cv2.imwrite('Cases/' + str(j//9) + str(j%9) + '.png', dst)
            else:
                print('Attention, la case ({}, {}) a été loupé.'.format(j//9, j%9))

            j += 1


def find_contours(img, blur, mode):
    if blur:
        img_blur = cv2.GaussianBlur(img,(3,3),1,1)
    else:
        img_blur = img
    #cv2.imwrite(f_debug + 'img_blur.png', img_blur)
    #img_canny = cv2.Canny(img_blur, 50, 150)
    if mode == 'wide':
        img_canny = cv2.Canny(img_blur, 10, 200)
    elif mode == 'tight':
        img_canny = cv2.Canny(img_blur, 225, 250)
    else:
        img_canny = convenience.auto_canny(img_blur)

    cv2.imwrite(f_debug + 'img_canny_grid.png', img_canny)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    dilated = cv2.dilate(img_canny, kernel)

    contours = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = adjust_contours(contours)

    cv2.imwrite(f_debug + 'dilated.png', dilated)

    return contours


def order_points(square):
    # On recupere le coin en haut a gauche
    som = [ sum(i) for i in square ]
    index = som.index(min(som))

    # On reordonne la liste des coordonnees pour commencer
    # par le point en haut a gauche
    pts_img = []
    for i in range(index, len(square)):
        pts_img.append(square[i])
    for i in range(0,index):
        pts_img.append(square[i])

    pts_img = np.array(pts_img, dtype = np.float32)

    return pts_img


class Error(Exception):
   """Base class for other exceptions"""
   pass


class GridNotRecognized(Error):
   """Raised when the main square of the grid is not recognized."""
   pass


def find_square(contour):
    c = sorted(contour, key = cv2.contourArea, reverse = True)

    # We assume the biggest area recognized is the sudoku
    peri = cv2.arcLength(c[0], True)
    # We limit the contour to 4 points
    i = 1
    while 'square does not contain 4 points':
        square = cv2.approxPolyDP(c[0], i * 0.01 * peri, True)
        i += 1
        if len(square) == 4 or i > 15000:
            break
    
    if i > 15000:
        raise GridNotRecognized

    square = np.array([list(i[0]) for i in square])

    return order_points(square)


def warp_square(img, h, pts_img):
    h = int(h)
    pts_square = np.array([[0, 0], [0, h], [h, h], [h, 0]], dtype = np.float32)
    M = cv2.getPerspectiveTransform(pts_img,pts_square)
    return cv2.warpPerspective(img, M, (h, h))


def adjust_contours(cnts):
    # Handling of different versions of opencv
    return cnts[0] if len(cnts) == 2 else cnts[1]


def local_max(array):
    """
    Returns the indexes of the local maximums, 
    meaning it is bigger than its previous value
    and its next value.
    """
    maxis = []
    # First number
    if array[0] > array[1]:
        maxis.append(0)
    # Last number
    if array[-1] > array[-2]:
        maxis.append(len(array) - 1)
    # The rest
    for i in range(1,len(array)-1):
        if array[i] > array[i-1] and array[i] > array[i+1]:
            maxis.append(i)
    
    return maxis


def clean(gray):
    """
    Removes the noise from an image. It detects contours,
    and then paints in white the contours that are smaller than
    the biggest one. Resizes the image to a 28*28, and removes black contours.
    """
    # Find contours
    cnts = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = adjust_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    # Paint every contour except the biggest one
    img = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
    for c in cnts[2:]:
        cv2.drawContours(img, [c], -1, (255,255,255), -1)

    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (28, 28), interpolation = cv2.INTER_AREA)

    # Remove black along the edges
    for i in range(28):
        img[i][27] = 255
        img[i][0] = 255
        img[27][i] = 255
        img[0][i] = 255

    return img


def trieur():
    div = os.listdir(f_cases)
    div = [a for a in div if '.png' in a]

    erase_create(f_numbers)

    average = []

    for p in div:
        img = cv2.imread(f_cases + p, 0)
        img_bin = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,57,5)
        
        moy = np.mean(np.array(img_bin))
        average.append(moy)

    # Getting the spikes in the histogram to be able to
    # find a value to sort out white cells from numbers
    numbers, values = np.histogram(average, bins=[200 + 5*i for i in range(12)])

    indexes = local_max(numbers)
    
    if len(indexes) > 1:
        seuil = (values[indexes[0]] + values[indexes[-1]])/2
    else:
        seuil = 235

    # Now we can sort the cells
    for p in div :
        img = cv2.imread(f_cases + p)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_bin = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,57,5)
        img_bin = clean(img_bin)

        moy = np.mean(np.array(img_bin))

        if moy < seuil:
            cv2.imwrite(f_numbers + p, img_bin)
        # else:
            # cv2.imwrite(f_numbers + 'blank' + p, img_bin)
            # cv2.imwrite('DATA_COMPUTED/' + str(randint(10000,1000000)) + '.png', img_bin)


def erase_create(folder):
    """
    Checks if a given folder exists, deletes it if so,
    and creates a new one after
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def printS(grid):
    g = [[str(i) for i in a] for a in grid]
    g = [' '.join(a) for a in g]
    print('\n'.join(g))
