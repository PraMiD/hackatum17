import numpy as np
import math
from PIL import Image

np.set_printoptions(threshold="Nan", linewidth="Nan")

def colorToBw(array):
    """
    Converts a color image to a black and white image.
    """
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = math.sqrt(sum(array[row,col]/3.0))
    return new_array

def colorToSingleColor(array, color):
    """
    Converst a colo image to a black and white image of a specific color.
    #color -> 0 == red; 1 == green; 2 == blue
    """
    return array[:,:,color]

def apply3filter(array, filter_):
    """
    Applies a symmetric (3x3, 5x5, etc.) filter to the array.
    """
    s = int(len(filter_)/2)
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height,width)))
    for row in range(s, (height-s)):
        for col in range(s, (width-s)):
            new_array[row,col] = np.sum(filter_ * array[(row-s):(row+s+1),(col-s):(col+s+1)])
    return new_array

def pythagoras(array1, array2):
    """
    Calculates the length of the hypothenuses to each pixels x and y values.
    """
    width = len(array1[0])
    height = len(array1)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = math.sqrt(pow(array1[row,col],2) + pow(array2[row,col],2))
    return new_array

def maxBw(array, value):
    """
    Scales an array so that the highest pixel value is equal to the parameter value.
    """
    m = np.max(array)
    c = value
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = (array[row,col]/float(m)) * c
    return new_array

def darken(array, amount):
    """
    Reduces the values of a matrix by a percentage (amount, e.g. 0.4 -> 40%) of the brightest pixel.
    """
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    m = np.max(array) * amount
    for row in range(height):
        for col in range(width):
            new_array[row, col] = ((array[row,col] - m) if (array[row,col] >= m) else (0))
    return new_array

def threshold(array, value):
    """
    Applies a threshold to the array, that sets every pixel which value is less
    that the paramenter value to 0. All the other pixels keep their values.
    """
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row,col] = (array[row,col] if (array[row,col] > value) else 0)
    return new_array

def soloEdge(array):
    """
    Reduces all Edges to 1 pixel in width.
    """
    width = len(array[0])
    height = len(array)
    new_array1 = np.array(np.zeros((height, width)))
    new_array2 = np.array(np.zeros((height, width)))
    new_array = np.array(np.zeros((height, width)))

    for row in range(height - 1):
        for col in range(width - 1):
            new_array1[row, col] = (array[row, col] if (array[row, col] > array[row,col - 1]) and (array[row, col] > array[row,col + 1]) else 0)

    for row in range(height - 1):
        for col in range(width - 1):
            new_array2[row, col] = (array[row, col] if (array[row, col] > array[row - 1,col]) and (array[row, col] > array[row + 1,col]) else 0)

    return (new_array1 + new_array2)