import os
import sys
import random
import numpy as np
import math
from PIL import Image
import json
import argparse

parser = argparse.ArgumentParser(description='Script to create new learning data by pasting given logos to random pictures.')
parser.add_argument('--frames', type=str, required=True, help='Path to the directory containing the random frames we use as background for the new data.')
parser.add_argument('--outdir', type=str, required=True, help='Path to an EXISTING directory where we copy the newly created data to.')
parser.add_argument('--logometa', type=str, required=True, help='Path to an JSON file containing the logo metadata.')
parser.add_argument('--samples', type=int, required=True, help='Number of new samples to create.')

args = parser.parse_args()



files = args.frames
outdir = args.outdir
config = json.load(open(args.logometa, "r"))

no = int(args.samples)
random.shuffle(files)
for f in files:
    f = os.path.join(args.frames, f)
    no -= 1

    with Image.open(f) as fd:
        # 0 uppen left
        # 1 upper right
        # 2 lower left
        # 3 lower right
        fd = fd.resize((720,405))
        width = int(fd.size[0])
        height = int(fd.size[1])

        for key in config.keys():
            if not os.path.exists(os.path.join(outdir, key)):
                os.makedirs(os.path.join(outdir, key))
                with open(os.path.join(outdir,key, "metadata.txt"), "w+") as mf:
                    mf.write("{},{},{},{},{}".format(key, config[key]["x"], config[key]["y"], width, height))
            logo = Image.open(key+".png")
            new_img = fd.copy()
            new_img.paste(logo, (config[key]["x"], config[key]["y"]), logo)
            

            if config[key]["pos"] == 0:
                new_img.crop((0, 0, width * 0.2, height * 0.2)).save(os.path.join(outdir, key, str(no) + ".jpg"), format='JPEG', subsampling=0, quality=100)
            elif config[key]["pos"] == 1:
                new_img.crop((width - width * 0.2, 0, width, height * 0.2)).save(os.path.join(outdir, key + "/" + str(no) + ".jpg"), format='JPEG', subsampling=0, quality=100)
            new_img.close()
        fd.close()

    if no == 0:
        break