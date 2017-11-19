import sys
import imageSource
import os
import csv
import numpy as np
from PIL import Image

horizontal_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int)
vertical_filter = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int)

sampleImage = Image.open("../../foo/10106_2017-11-07_11.34.09_8.jpg")

imgArray = np.asarray(sampleImage)
array3h = imageSource.apply3filter(imageSource.colorToBw(imgArray), horizontal_filter)
array3v = imageSource.apply3filter(imageSource.colorToBw(imgArray), vertical_filter)
Image.fromarray(np.uint8(imageSource.threshold(imageSource.maxBw(imageSource.pythagoras(array3h,array3v),255), 30))).save("../../brHD_test.jpg")