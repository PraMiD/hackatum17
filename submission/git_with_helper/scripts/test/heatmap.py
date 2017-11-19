import sys
import imageSource
import os
import csv
import numpy as np
from PIL import Image
from PIL import ImageDraw

horizontal_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int)
vertical_filter = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int)

if len(sys.argv) < 2:
    print("Insufficient parameter given. Expects [extract_logo] train_data_path")
    sys.exit(1)
else:
    trainPath = sys.argv[1]

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
                    positions[(x,y,w,h)] = 0

                # walk over all samples
                for i, sample in enumerate(os.listdir(logoPath)):
                    if sample.endswith(".jpg"):
                        positions[(x,y,w,h)] += 1

# Print the heatmap on a 720x405 image to display spaces with most logos
heatmap = Image.new('RGBA', (720, 405), (255,255,255,255))

for k, v in positions.items():
    x, y, w, h = k
    poly = Image.new('RGBA', (720,405))
    pdraw = ImageDraw.Draw(poly)
    pdraw.rectangle([(x,y),(x+w,y+h)], fill=(255,0,0,int(v / 60)))
    heatmap.paste(poly, mask=poly)

heatmap.save("heatmap.png")
