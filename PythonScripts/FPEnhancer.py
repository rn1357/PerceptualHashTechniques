#fingerprint_enhancer library used from  https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python
import fingerprint_enhancer					# Load the library 
import cv2, os, sys
import numpy as np

def fingerPrintEnhancer(input_imgfolderpath, output_imgfolderpath):
    for imgpath in input_imgfolderpath:
        img_name = imgpath.split("/")[-1].split("_")[0]
        image = cv2.imread(imgpath)
        out = fingerprint_enhancer. enhance_Fingerprint(image) #enhance the image using fingerprint_enhancer library
        f_image = cv2.resize(out, (448, 480))
        cv2.imwrite(output_imgfolderpath + f'{img_name}.jpg', f_image)#files will be stored as file numbers corresponding to the raw file

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folderpath = sys.argv[2]
    input_folderpath = []
    dirs = os.listdir(input_folder)
    for file in dirs:
        if file.endswith(".bmp"):
            input_folderpath.append(os.path.join(input_folder, file))
    fingerPrintEnhancer(input_folderpath, output_folderpath)

