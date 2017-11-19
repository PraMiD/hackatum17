import sys
import imageSource
import os
import csv
import numpy as np
from PIL import Image

"""
    This script is capable of extracting the logos of images.
    It depends on the old version of the image manipulation library,
    which is included to offer reproducibility of our data.
"""
horizontal_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int)
vertical_filter = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int)


"""
    Simple filter is applied to the image:
    | -1 | 0 | 1 |
    | -1 | 0 | 1 |
    | -1 | 0 | 1 |

    Its low size leads to efficient computation times,
    but it is nevertheless capable of detecting edges with 
    sufficient reliability.
"""
def filterLogo(img, x, y, w, h):
    imgArray = np.asarray(img)[y-1:y+h+1, x-1:x+w+1]
    array3h = imageSource.apply3filter(imageSource.colorToBw(imgArray), horizontal_filter)
    array3v = imageSource.apply3filter(imageSource.colorToBw(imgArray), vertical_filter)
    return Image.fromarray(np.uint8(imageSource.threshold(imageSource.maxBw(imageSource.pythagoras(array3h,array3v),255), 30))[1:h,1:w])

if len(sys.argv) < 3:
    print("Insufficient parameter given. Expects [extract_logo] train_data_path logo_repo_path")
    sys.exit(1)
else:
    trainPath = sys.argv[1]
    repoPath = sys.argv[2]

METADATA_FILE = "metadata.txt"

positions = {}

# walk over all stations
for station in os.listdir(trainPath):
    stationPath = os.path.join(trainPath, station)
    # walk over all logo types
    for logo in os.listdir(stationPath):
        # see if there is a meta data file or no logo is expected
        logoPath = os.path.join(stationPath, logo)
        metadata_file_path = os.path.join(logoPath, METADATA_FILE)
        print(metadata_file_path)

        if os.path.exists(metadata_file_path):
            # read the metadata
            with open(metadata_file_path) as metadata:
                reader = csv.reader(metadata, delimiter=',')
                line = list(reader)[len(list(reader))-1]
                c = line[0]
                x, y, w, h = [int(a) for a in line[1:]]
                
                if not (x,y,w,h) in positions:
                    positions[(x,y,w,h)] += 1
                else:
                    positions[(x,y,w,h)] = 1
                images = []

                # walk over all samples
                for i, sample in enumerate(os.listdir(logoPath)):
                    if sample.endswith(".jpg"):
                        imagePath = os.path.join(logoPath, sample)
                        print("Working on file {}".format(imagePath))

                        sampleImage = Image.open(imagePath)

                        # run filters if size is reasonable
                        width, height = sampleImage.size
                        if x+w > width or y+h > height:
                            continue
                        sampleImage = filterLogo(sampleImage,x,y,w,h)
                        
                        # save for median image
                        #images.append(sampleImage)

                        # store result
                        if not os.path.exists(os.path.join(repoPath, c)):
                            os.makedirs(os.path.join(repoPath, c))
                            
                        sampleImage.save(os.path.join(repoPath, c, "{}_{}_{}_{}_{}_{}.png".format(c,x,y,w,h,i)))
                        print("> saving: " + os.path.join(repoPath, c, "{}_{}_{}_{}_{}_{}.png".format(c,x,y,w,h,i)))
