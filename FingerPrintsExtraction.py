#import fingerprint_feature_extractor
#import cv2
#image = cv2.imread('/Users/rakshithanagendrappa/Desktop/1.jpg',0)
#FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor. extract_minutiae_features (image, spuriousMinutiaeThresh=10, invertImage=False, showResult=True, saveResult=True) 
import fingerprint_feature_extractor
import cv2
import numpy as np
import glob
input_path = r"/Users/rakshithanagendrappa/Desktop/enhanced/*.jpg"
out_path = '/Users/rakshithanagendrappa/Desktop/extracted/'
image_paths = list(glob.glob(input_path))
for i,img in enumerate(image_paths):
    image = cv2.imread(img)
    FeaturesTerminations[i], FeaturesBifurcations[i] = fingerprint_feature_extractor. extract_minutiae_features (image, spuriousMinutiaeThresh=10, invertImage=False, showResult=True, saveResult=True) 
    cv2.imwrite(out_path + f'{str[i+1]}.jpg',(FeaturesTerminations[i], FeaturesBifurcations[i]))
