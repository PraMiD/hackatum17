import numpy as np
import math
from PIL import Image
from ImageSource import *
import os
from multiprocessing import Pool

source = "/Users/moritz/Desktop/Edge Approach 01/SWR/logo1"
destination = "SWR/logo1_cut"
c = 0.2
cuts = [[0.0,c,0.0,c],[0.0,c,1-c,1.0],[1-c,1.0,0.0,c],[1-c,1.0,1-c,1.0]]

np.set_printoptions(threshold="Nan", linewidth="Nan")

files = os.listdir(source)
files = [x for x in files if not x.startswith('.')]

def corner(f):
    pic = Image.open("%s/%s" % (source,f[1]))
    array = np.asarray(pic)
    width = len(array[0])
    height = len(array)
    for j in range(4):
        if j == 0:
            array2 = my_canny(array[int(cuts[j][0] * height):int(cuts[j][1] * height),
                                    int(cuts[j][2] * width):int(cuts[j][3] * width)])
            pic2 = Image.fromarray(np.uint8(array2))
            pic2.save("%s/cut_%.4d.png" % (destination,f[0]))

p = Pool(processes = 8)

p.map(corner, enumerate(files))
