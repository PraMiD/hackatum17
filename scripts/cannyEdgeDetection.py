# -*- coding: utf-8 -*_

import numpy as np
from PIL import Image
#from multiprocessing import Pool

np.set_printoptions(threshold = "Nan", linewidth= "Nan")

im = Image.open("/Users/moritzmakowski/Desktop/Canny Edeg Detection/20130101_PN_JB3.jpg")
a = np.asarray(im)
width = len(a[0])
height = len(a)
print "Width:  ", width
print "Height: ", height

b = np.zeros((len(a), len(a[0])), dtype = np.int8)
c = np.zeros((len(a), len(a[0])), dtype = np.int8)
d = np.zeros((len(a), len(a[0]), 3), dtype = np.int8)
topvalue = 0
#print a[0:20,0:20]

for row in range(len(a)):
	for col in range(len(a[0])):
		p = a[row,col]
		value = (p[0] + p[1])/2.0
		b[row,col] = value

#print b[0:20,0:20]
		
for row in range(1, len(b) - 1):
	for col in range(1, len(b[0]) - 1):
		horizontal  = b[row    , col - 1] - b[row    , col + 1]
		horizontal += b[row - 1, col - 1] - b[row - 1, col + 1]
		horizontal += b[row + 1, col - 1] - b[row + 1, col + 1]
		
		vertical  = b[row - 1, col    ] - b[row + 1, col    ]
		vertical += b[row - 1, col - 1] - b[row + 1, col - 1]
		vertical += b[row - 1, col + 1] - b[row + 1, col + 1]
		
		value = abs(vertical) + abs(horizontal)
		#value = 255 if (value > 255) else value
		if value > topvalue:
			topvalue = value
		c[row, col] = value

for row in range(1, len(b) - 1):
	for col in range(1, len(b[0]) - 1):
		value = (c[row, col]/float(topvalue)) * 255
		d[row, col] = [value,value,value]
		
		
pic = Image.fromarray(np.uint8(c))
pic.show()
#pic.save("CannyRedGreen.png")