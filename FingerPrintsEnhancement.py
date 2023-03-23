import fingerprint_enhancer					# Load the library 
import cv2 
import numpy as np
import glob
input_path = r"/Users/rakshithanagendrappa/Desktop/Distorted/*.bmp"
out_path = '/Users/rakshithanagendrappa/Desktop/DistortedEnhanced/'

image_paths = list(glob.glob(input_path))
for i, img in enumerate(image_paths):
    img_name = img.split("/")[-1].split("_")[0]
    image = cv2.imread(img)
    out = fingerprint_enhancer. enhance_Fingerprint(image) 
    f_image = cv2.resize(out, (448, 480))
    cv2.imwrite(out_path + f'{img_name}.jpg', f_image)
