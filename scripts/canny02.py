import numpy as np
import math
from PIL import Image

np.set_printoptions(threshold="Nan", linewidth="Nan")
pic = Image.open("/Users/moritz/Desktop/Python 3.6/PyCharm Projects/Canny02/10906_2017-11-06_19.03.12_0.jpg")
array1 = np.asarray(pic)

my_filter = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.int) * 10
my_filter2 = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.int) * 10

def colorToBw(array):
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = math.sqrt(sum(array[row,col]/3.0))
    return new_array

def apply3filter(array, filter_):
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height,width)))
    for row in range(1, (height-1)):
        for col in range(1, (width-1)):
            new_array[row,col] = np.sum(filter_ * array[(row-1):(row+2),(col-1):(col+2)])
    return new_array

def pythagoras(array1, array2):
    width = len(array1[0])
    height = len(array1)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = math.sqrt(pow(array1[row,col],2) + pow(array2[row,col],2))
    return new_array

def maxBw(array):
    m = np.max(array)
    c = 255
    width = len(array1[0])
    height = len(array1)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = (array[row,col]/float(m)) * c
    return new_array


def threshold(array, value):
    width = len(array1[0])
    height = len(array1)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = (array[row,col] if (array[row,col] > value) else 0)
    return new_array

array2 = colorToBw(array1)

array3v = apply3filter(array2,my_filter)
array3h = apply3filter(array2,my_filter2)


array4 = threshold(maxBw(pythagoras(array3h,array3v)),50)

"""
print array3v[0:10,0:10]
print "*" * 30
print array3h[0:10,0:10]
print "*" * 30
print array4[0:10,0:10]
"""

pic2 = Image.fromarray(np.uint8(array4))
pic2.show()
pic2.save("Test4.png")