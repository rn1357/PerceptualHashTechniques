#Fingerprint orientation map extractor code used from https://github.com/rayronvictor/Fingerprint-Features-Extraction/blob/master/orientation.py
import cv2 
import numpy as np 
import math
import os, sys
from matplotlib import pyplot as plt 
 
f = lambda x,y: 2*x*y 
g = lambda x,y: x**2 - y**2 
 
def get_line_ends(x, y, tang, block_size, offset=0): 
    x, y = x*block_size, y*block_size 
    half_block = (block_size/float(2)) 

    if offset < 0: 
        offset = 0 
    elif offset > block_size/2: 
        offset = block_size/2 

    if -1 <= tang <= 1: 
        x1 = x + offset 
        y1 = y + half_block - (tang * half_block) 
        x2 = x + block_size - offset 
        y2 = y + half_block + (tang * half_block) 
    else: 
        x1 = x + half_block + (half_block/(2*tang)) 
        y1 = y + block_size - offset 
        x2 = x + half_block - (half_block/(2*tang)) 
        y2 = y + offset 
    return (int(round(x1)), int(round(y1))), (int(round(x2)), int(round(y2))) 
 
def draw_lines(h, w, c, angles, block_size): 
    im = np.empty((h, w, c), np.uint8) 
    # white background 
    im[:] = 255 

    for i in range(int(w/block_size)): 
        for j in range(int(h/block_size)): 
            angle = angles.item(j, i) 
            if angle != 0: 
                angle = -1/math.tan(math.radians(angle)) 
                p1, p2 = get_line_ends(i, j, angle, block_size, 2) 
                cv2.line(im, p1, p2, (0,0,255), 1) 
    return im 
 
def orientation(img, block_size, smooth=False): 
    h, w = img.shape 

    # make a reflect border frame to simplify kernel operation on borders 
    borderedImg = cv2.copyMakeBorder(img, block_size,block_size,block_size,block_size, cv2.BORDER_DEFAULT) 

    # apply a gradient in both axis 
    sobelx = cv2.Sobel(borderedImg, cv2.CV_64F, 1, 0, ksize=3) 
    sobely = cv2.Sobel(borderedImg, cv2.CV_64F, 0, 1, ksize=3) 
    angles = np.zeros((int(h/block_size), int(w/block_size)), np.float32) 
    for i in range(int(w/block_size)): 
        for j in range(int(h/block_size)): 
            nominator = 0. 
            denominator = 0. 

        # calculate the summation of nominator (2*Gx*Gy) 
        # and denominator (Gx^2 - Gy^2), where Gx and Gy 
        # are the gradient values in the position (j, i) 
            for k in range(block_size): 
                for l in range(block_size): 
                    posX = block_size-1 + (i*block_size) + k 
                    posY = block_size-1 + (j*block_size) + l 
                    valX = sobelx.item(posY, posX) 
                    valY = sobely.item(posY, posX) 

                    nominator += f(valX, valY) 
                    denominator += g(valX, valY) 

            # if the strength (norm) of the vector  
            # is not greater than a threshold 
            if math.sqrt(nominator**2 + denominator**2) < 1000000: 
                angle = 0. 
            else: 
                if denominator >= 0: 
                    angle = cv2.fastAtan2(nominator, denominator) 
                elif denominator < 0 and nominator >= 0: 
                    angle = cv2.fastAtan2(nominator, denominator) + math.pi 
                else: 
                    angle = cv2.fastAtan2(nominator, denominator) - math.pi 
                angle /= float(2) 

            angles.itemset((j, i), angle) 

    if smooth: 
        angles = cv2.GaussianBlur(angles, (3,3), 0, 0) 
    return angles 
 
def draw_orientation(h, w, angles, block_size): 
    im = np.zeros((h, w), np.uint8) 
    for i in range(int(w/block_size)): 
        for j in range(int(h/block_size)):  
            dangle = 2*angles.item(j, i) 
            v = int(round(dangle * (255/float(360)))) 
            for k in range(block_size): 
                for l in range(block_size): 
                    im.itemset((j*block_size+l,i*block_size+k), v) 
    return im 
 
if __name__ == '__main__': 
    input_folder = sys.argv[1]
    out_folderpath = sys.argv[2]
    input_folderpath = []
    dirs = os.listdir(input_folder)
    for file in dirs:
        if file.endswith(".bmp"):
            input_folderpath.append(os.path.join(input_folder , file))       
    for imgpath in input_folderpath:
        KSIZE = 11  
        img_name = imgpath.split("/")[-1].split("_")[0]
        image = cv2.imread(imgpath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        angles = orientation(gray, KSIZE) 
        h, w = gray.shape  
        orientationImg = draw_lines(h, w, 3, angles, KSIZE) 
        orientation_draw = draw_orientation(h, w, angles, KSIZE)  
        cv2.imwrite(out_folderpath + f'{img_name}.jpg', orientationImg) 


