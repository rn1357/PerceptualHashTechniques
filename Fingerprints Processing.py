import fingerprint_enhancer 
import cv2 
import numpy as np
import skimage.morphology
from skimage.morphology import convex_hull_image, erosion
from skimage.morphology import square
import math
from matplotlib import pyplot as plt
from PIL import Image
import imagehash
import csv,os,sys


#fingerprint_enhancer library used from  https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python
def fingerPrintEnhancer(image, enhanced_output_loc):
    out = fingerprint_enhancer. enhance_Fingerprint(image) 
    f_image = cv2.resize(out, (448, 480))
    cv2.imwrite(enhanced_output_loc, f_image)
    
    
#fingerprint_extraction code used from https://github.com/Utkarsh-Deshmukh/Fingerprint-Feature-Extraction
class MinutiaeFeature(object):
    def __init__(self, locX, locY, Orientation, Type):
        self.locX = locX
        self.locY = locY
        self.Orientation = Orientation
        self.Type = Type

class FingerprintFeatureExtractor(object):
    def __init__(self):
        self._mask = []
        self._skel = []
        self.minutiaeTerm = []
        self.minutiaeBif = []
        self._spuriousMinutiaeThresh = 10

    def setSpuriousMinutiaeThresh(self, spuriousMinutiaeThresh):
        self._spuriousMinutiaeThresh = spuriousMinutiaeThresh

    def __skeletonize(self, img):
        img = np.uint8(img > 128)
        self._skel = skimage.morphology.skeletonize(img)
        self._skel = np.uint8(self._skel) * 255
        self._mask = img * 255

    def __computeAngle(self, block, minutiaeType):
        angle = []
        (blkRows, blkCols) = np.shape(block)
        CenterX, CenterY = (blkRows - 1) / 2, (blkCols - 1) / 2
        if (minutiaeType.lower() == 'termination'):
            sumVal = 0
            for i in range(blkRows):
                for j in range(blkCols):
                    if ((i == 0 or i == blkRows - 1 or j == 0 or j == blkCols - 1) and block[i][j] != 0):
                        angle.append(-math.degrees(math.atan2(i - CenterY, j - CenterX)))
                        sumVal += 1
                        if (sumVal > 1):
                            angle.append(float('nan'))
            return (angle)

        elif (minutiaeType.lower() == 'bifurcation'):
            (blkRows, blkCols) = np.shape(block)
            CenterX, CenterY = (blkRows - 1) / 2, (blkCols - 1) / 2
            angle = []
            sumVal = 0
            for i in range(blkRows):
                for j in range(blkCols):
                    if ((i == 0 or i == blkRows - 1 or j == 0 or j == blkCols - 1) and block[i][j] != 0):
                        angle.append(-math.degrees(math.atan2(i - CenterY, j - CenterX)))
                        sumVal += 1
            if (sumVal != 3):
                angle.append(float('nan'))
            return (angle)

    def __getTerminationBifurcation(self):
        self._skel = self._skel == 255
        (rows, cols) = self._skel.shape
        self.minutiaeTerm = np.zeros(self._skel.shape)
        self.minutiaeBif = np.zeros(self._skel.shape)

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if (self._skel[i][j] == 1):
                    block = self._skel[i - 1:i + 2, j - 1:j + 2]
                    block_val = np.sum(block)
                    if (block_val == 2):
                        self.minutiaeTerm[i, j] = 1
                    elif (block_val == 4):
                        self.minutiaeBif[i, j] = 1

        self._mask = convex_hull_image(self._mask > 0)
        self._mask = erosion(self._mask, square(5))  # Structuing element for mask erosion = square(5)
        self.minutiaeTerm = np.uint8(self._mask) * self.minutiaeTerm

    def __removeSpuriousMinutiae(self, minutiaeList, img):
        img = img * 0
        SpuriousMin = []
        numPoints = len(minutiaeList)
        D = np.zeros((numPoints, numPoints))
        for i in range(1,numPoints):
            for j in range(0, i):
                (X1,Y1) = minutiaeList[i]['centroid']
                (X2,Y2) = minutiaeList[j]['centroid']

                dist = np.sqrt((X2-X1)**2 + (Y2-Y1)**2)
                D[i][j] = dist
                if(dist < self._spuriousMinutiaeThresh):
                    SpuriousMin.append(i)
                    SpuriousMin.append(j)

        SpuriousMin = np.unique(SpuriousMin)
        for i in range(0,numPoints):
            if(not i in SpuriousMin):
                (X,Y) = np.int16(minutiaeList[i]['centroid'])
                img[X,Y] = 1

        img = np.uint8(img)
        return(img)

    def __cleanMinutiae(self, img):
        self.minutiaeTerm = skimage.measure.label(self.minutiaeTerm, connectivity=2)
        RP = skimage.measure.regionprops(self.minutiaeTerm)
        self.minutiaeTerm = self.__removeSpuriousMinutiae(RP, np.uint8(img))

    def __performFeatureExtraction(self):
        FeaturesTerm = []
        self.minutiaeTerm = skimage.measure.label(self.minutiaeTerm, connectivity=2)
        RP = skimage.measure.regionprops(np.uint8(self.minutiaeTerm))

        WindowSize = 2  # --> For Termination, the block size must can be 3x3, or 5x5. Hence the window selected is 1 or 2
        FeaturesTerm = []
        for num, i in enumerate(RP):
            (row, col) = np.int16(np.round(i['Centroid']))
            block = self._skel[row - WindowSize:row + WindowSize + 1, col - WindowSize:col + WindowSize + 1]
            angle = self.__computeAngle(block, 'Termination')
            if(len(angle) == 1):
                FeaturesTerm.append(MinutiaeFeature(row, col, angle, 'Termination'))

        FeaturesBif = []
        self.minutiaeBif = skimage.measure.label(self.minutiaeBif, connectivity=2)
        RP = skimage.measure.regionprops(np.uint8(self.minutiaeBif))
        WindowSize = 1  # --> For Bifurcation, the block size must be 3x3. Hence the window selected is 1
        for i in RP:
            (row, col) = np.int16(np.round(i['Centroid']))
            block = self._skel[row - WindowSize:row + WindowSize + 1, col - WindowSize:col + WindowSize + 1]
            angle = self.__computeAngle(block, 'Bifurcation')
            if(len(angle) == 3):
                FeaturesBif.append(MinutiaeFeature(row, col, angle, 'Bifurcation'))
        return (FeaturesTerm, FeaturesBif)

    def extractMinutiaeFeatures(self, img):
        self.__skeletonize(img)

        self.__getTerminationBifurcation()

        self.__cleanMinutiae(img)

        FeaturesTerm, FeaturesBif = self.__performFeatureExtraction()
        return(FeaturesTerm, FeaturesBif)

    def showResults(self, FeaturesTerm, FeaturesBif):
        
        (rows, cols) = self._skel.shape
        DispImg = np.zeros((rows, cols, 3), np.uint8)
        DispImg[:, :, 0] = 255*self._skel
        DispImg[:, :, 1] = 255*self._skel
        DispImg[:, :, 2] = 255*self._skel

        for idx, curr_minutiae in enumerate(FeaturesTerm):
            row, col = curr_minutiae.locX, curr_minutiae.locY
            (rr, cc) = skimage.draw.circle_perimeter(row, col, 3)
            skimage.draw.set_color(DispImg, (rr, cc), (0, 0, 255))

        for idx, curr_minutiae in enumerate(FeaturesBif):
            row, col = curr_minutiae.locX, curr_minutiae.locY
            (rr, cc) = skimage.draw.circle_perimeter(row, col, 3)
            skimage.draw.set_color(DispImg, (rr, cc), (255, 0, 0))
        
        cv2.imshow('output', DispImg)
        cv2.waitKey(0)

    def saveResult(self, FeaturesTerm, FeaturesBif, img_loc):
        (rows, cols) = self._skel.shape
        DispImg = np.zeros((rows, cols, 3), np.uint8)
        DispImg[:, :, 0] = 255 * self._skel
        DispImg[:, :, 1] = 255 * self._skel
        DispImg[:, :, 2] = 255 * self._skel

        for idx, curr_minutiae in enumerate(FeaturesTerm):
            row, col = curr_minutiae.locX, curr_minutiae.locY
            (rr, cc) = skimage.draw.circle_perimeter(row, col, 3)
            skimage.draw.set_color(DispImg, (rr, cc), (0, 0, 255))

        for idx, curr_minutiae in enumerate(FeaturesBif):
            row, col = curr_minutiae.locX, curr_minutiae.locY
            (rr, cc) = skimage.draw.circle_perimeter(row, col, 3)
            skimage.draw.set_color(DispImg, (rr, cc), (255, 0, 0))
        cv2.imwrite(img_loc, DispImg)


def extract_minutiae_features(img, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=False, img_loc=None):
    feature_extractor = FingerprintFeatureExtractor()
    feature_extractor.setSpuriousMinutiaeThresh(spuriousMinutiaeThresh)
    if (invertImage):
        img = 255 - img;

    FeaturesTerm, FeaturesBif = feature_extractor.extractMinutiaeFeatures(img)

    if (saveResult):
        feature_extractor.saveResult(FeaturesTerm, FeaturesBif, img_loc)

    if(showResult):
        feature_extractor.showResults(FeaturesTerm, FeaturesBif)

    return(FeaturesTerm, FeaturesBif)




#orientation maps extraction code from https://github.com/rayronvictor/Fingerprint-Features-Extraction/blob/master/orientation.py 
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

    
if __name__ == "__main__":
    for i in sys.argv[1:3]:
        input_folder = i
        #normal
        if i == sys.argv[1]:
            enhanced_output_imgfolderpath = sys.argv[3]#enhanced o/p
            extracted_output_folderpath = sys.argv[4]#extracted o/p
            orientation_output_folderpath = sys.argv[5]#oriented o/p
        #distorted    
        if i == sys.argv[2]:
            enhanced_output_imgfolderpath = sys.argv[6]#enhanced o/p
            extracted_output_folderpath = sys.argv[7]#extracted o/p
            orientation_output_folderpath = sys.argv[8]#oriented o/p
            
        raw_input_imgfolderpath = []
        dirs = os.listdir(input_folder)
        for file in dirs:
            if file.endswith(".bmp"):
                raw_input_imgfolderpath.append(os.path.join(input_folder, file))
        for imgpath in raw_input_imgfolderpath:
            img_name = imgpath.split("/")[-1].split("_")[0]
            image = cv2.imread(imgpath)
            enhanced_output_loc = enhanced_output_imgfolderpath + f'{img_name}.jpg'
            fingerPrintEnhancer(image, enhanced_output_loc)

        extracted_input_folderpath = []
        extracted_dirs = os.listdir(enhanced_output_imgfolderpath)
        for file in extracted_dirs:
            if file.endswith(".jpg"):
                extracted_input_folderpath.append(os.path.join(enhanced_output_imgfolderpath, file))
        for imgpath in extracted_input_folderpath:
            img_name = imgpath.split("/")[-1].split("_")[0]
            image = cv2.imread(imgpath)
            grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_loc = extracted_output_folderpath + f'{img_name}'
            FeaturesTerminations, FeaturesBifurcations = extract_minutiae_features (grayscale, spuriousMinutiaeThresh=10, invertImage=False, showResult=False, saveResult=True, img_loc=img_loc)

        for imgpath in raw_input_imgfolderpath:
            KSIZE = 11  
            img_name = imgpath.split("/")[-1].split("_")[0]
            image = cv2.imread(imgpath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            angles = orientation(gray, KSIZE) 
            h, w = gray.shape  
            orientationImg = draw_lines(h, w, 3, angles, KSIZE) 
            orientation_draw = draw_orientation(h, w, angles, KSIZE)  
            cv2.imwrite(orientation_output_folderpath + f'{img_name}.jpg', orientationImg) 
