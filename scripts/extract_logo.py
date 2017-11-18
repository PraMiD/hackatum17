import sys
import imageSource
import os
import csv
import numpy as np
from PIL import Image

horizontal_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int)
vertical_filter = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int)

def filterLogo(img, x, y, w, h):
    imgArray = np.asarray(img)[y-1:y+h+1, x-1:x+w+1]
    array3h = imageSource.apply3filter(imageSource.colorToBw(imgArray), horizontal_filter)
    array3v = imageSource.apply3filter(imageSource.colorToBw(imgArray), vertical_filter)
    return Image.fromarray(np.uint8(imageSource.threshold(imageSource.maxBw(imageSource.pythagoras(array3h,array3v),255), 30)))

if len(sys.argv) < 3:
    print("Insufficient parameter given. Expects [extract_logo] train_data_path logo_repo_path")
    sys.exit(1)
else:   
    trainPath = sys.argv[1]
    repoPath = sys.argv[2]

METADATA_FILE = "metadata.txt"

positions = set()

# walk over all stations
for station in os.listdir(trainPath):
    path = os.path.join(trainPath, station)
    # walk over all logo types
    for logo in os.listdir(path):
        # see if there is a meta data file or no logo is expected
        path = os.path.join(path, logo)
        metadata_file_path = os.path.join(path, METADATA_FILE)
        if os.path.exists(metadata_file_path):
            # read the metadata
            with open(metadata_file_path) as metadata:
                reader = csv.reader(metadata, delimiter=',')
                line = next(reader)
                c = line[0]
                x, y, w, h = [int(a) for a in line[1:]]
                
                positions.add((x,y,w,h))
                
                # walk over all samples
                for sample in os.listdir(path):
                    if sample.endswith(".jpg"):
                        imagePath = os.path.join(path, sample)
                        print("Working on file {}".format(imagePath))

                        sampleImage = Image.open(imagePath)

                        # run filters
                        sampleImage = filterLogo(sampleImage,x,y,w,h)
                        sampleImage.save("test.png")


