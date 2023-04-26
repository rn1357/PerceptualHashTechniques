# PerceptualHashTechniques
Evaluation of perceptual hash techniques for biometric fingerprint authentication

Steps for execution:
1. User should input the normal fringerprints folder path ex: /*/Desktop/NormalExtracted/
2. User should input the distorted fingerprints folder path ex: /*/Desktop/DistortedExtracted/
3. User should input the type of hash function/technique to compute(average_hash/phash/dhash/whash)
4. User should input the output file path to store the output for robustness ex: /*/AverageHashHammingDistancesforRobustness.csv
5. User should input the output file path to store the output for discrimination capability ex: /*/AverageHashHammingDistancesforDiscrimination.csv


Fingerprint enhancement and fingerprint extraction code is referenced by https://github.com/Utkarsh-Deshmukh/Fingerprint-Enhancement-Python and https://github.com/Utkarsh-Deshmukh/Fingerprint-Feature-Extraction

Orientation Map extraction was done with the help of : https://github.com/rayronvictor/Fingerprint-Features-Extraction/blob/master/orientation.py
Fingerprint database used http://ivg.au.tsinghua.edu.cn/dataset/TDFD.php

Xuanbin Si, Jianjiang Feng, Jie Zhou, Yuxuan Luo, "Detection and rectification of distorted fingerprints", IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 37, no. 3, pp. 555-568, 2015.

Hash techniques library usage was referenced by https://github.com/JohannesBuchner/imagehash
