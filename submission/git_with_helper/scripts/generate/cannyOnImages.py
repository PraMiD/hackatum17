import sys
import imageSource
import os
import csv
import numpy as np
from PIL import Image
from multiprocessing import Pool

horizontal_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int)
vertical_filter = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int)

def filterLogo(img):
    imgArray = np.asarray(img)
    array3h = imageSource.apply3filter(imageSource.colorToBw(imgArray), horizontal_filter)
    array3v = imageSource.apply3filter(imageSource.colorToBw(imgArray), vertical_filter)
    return Image.fromarray(np.uint8(imageSource.threshold(imageSource.maxBw(imageSource.pythagoras(array3h,array3v),255), 30)))


def canny(imagePath):
    print(imagePath)
    c = imagePath.split('/')[-2]
    sampleImage = Image.open(imagePath)
    sampleImage = filterLogo(sampleImage)
    if not os.path.exists(os.path.join(repoPath, c)):
        os.makedirs(os.path.join(repoPath, c))

    sampleImage.save(os.path.join(repoPath, c, os.path.basename(imagePath)))
    print("> saving: " + os.path.join(repoPath, c, os.path.basename(imagePath)))

if len(sys.argv) < 3:
    print("Insufficient parameter given. Expects [extract_logo] train_data_path logo_repo_path")
    sys.exit(1)
else:
    trainPath = sys.argv[1]
    repoPath = sys.argv[2]

METADATA_FILE = "metadata.txt"

positions = {}
todo = []

# walk over all stations
for logo in os.listdir(trainPath):
    if logo == "br":
        continue
    # see if there is a meta data file or no logo is expected
    logoPath = os.path.join(trainPath, logo)
    # walk over all samples
    for i, sample in enumerate(os.listdir(logoPath)):
        if sample.endswith(".jpg"):
            todo.append(os.path.join(logoPath, sample))


p = Pool(4)
p.map(canny, todo)

