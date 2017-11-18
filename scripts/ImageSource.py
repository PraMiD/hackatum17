import numpy as np
import math
from PIL import Image

np.set_printoptions(threshold="Nan", linewidth="Nan")

canny_filter_horizontal = np.array([[ 1, 1, 1],
                                    [ 0, 0, 0],
                                    [-1,-1,-1]],dtype = np.int)
canny_filter_vertical = np.array([[1,0,-1],
                                  [1,0,-1],
                                  [1,0,-1]],dtype = np.int)

def color_to_bw(array):
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

def color_to_single_color(array, color):
    """
    Converst a colored image to a black and white image of a specific color.
    #color -> 0 == red; 1 == green; 2 == blue
    """
    return array[:,:,color]

def color_to_dual_color(array, color1, color2):
    """
        Converst a colored image to a black and white image of two specific colors.
        #color -> 0 == red; 1 == green; 2 == blue
        """
    width = len(array[0])
    height = len(array)
    new_array = np.array(np.zeros((height, width)))
    for row in range(height):
        for col in range(width):
            new_array[row, col] = math.sqrt(sum(array[row, col,0:2] / 2.0))
    return new_array

def apply_filter(array, filter_):
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

def maxBw(array, value = 255):
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

def darken(array, amount = 0.7):
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

def edgeApproach(array, noise = 0.4):
    width = len(array[0])
    height = len(array)
    top = 0
    top_ = True
    bottom = 0
    bottom_ = True
    left = 0
    left_ = True
    right = 0
    right_ = True
    average = np.sum(array)/(float(width * height))

    while (top_ or bottom_ or left_ or right_):
        if top_ and ((np.sum(array[top])/width) < (noise * average)):
            top += 1
        else:
            top_ = False

        if bottom_ and ((np.sum(array[height - bottom - 1])/width) < (noise * average)):
            bottom += 1
        else:
            bottom_ = False

        if left_ and ((np.sum(array.T[left])/height) < (noise * average)):
            left += 1
        else:
            left_ = False

        if right_ and ((np.sum(array.T[width - right - 1])/width) < (noise * average)):
            right += 1
        else:
            right_ = False

    return array[top:(height-bottom),left:(width-right)]

def symmetric_canny(array):
    arrayh = apply_filter(array,canny_filter_horizontal)
    arrayv = apply_filter(array,canny_filter_vertical)
    return (pythagoras(arrayh,arrayv))

def array_size(array):
    return (len(array) * len(array[0]))

def my_canny(array):
    array1 = edgeApproach(maxBw(symmetric_canny(darken(color_to_single_color(array,0)))))
    array2 = edgeApproach(maxBw(symmetric_canny(darken(color_to_single_color(array,1)))))
    array3 = edgeApproach(maxBw(symmetric_canny(darken(color_to_single_color(array,2)))))
    array4 = edgeApproach(maxBw(symmetric_canny(darken(color_to_dual_color(array,0,1)))))
    array5 = edgeApproach(maxBw(symmetric_canny(darken(color_to_dual_color(array,1,2)))))
    array6 = edgeApproach(maxBw(symmetric_canny(darken(color_to_dual_color(array,0,2)))))
    array7 = edgeApproach(maxBw(symmetric_canny(darken(color_to_bw(array)))))
    size1 = array_size(array1)
    size2 = array_size(array2)
    size3 = array_size(array3)
    size4 = array_size(array4)
    size5 = array_size(array5)
    size6 = array_size(array6)
    size7 = array_size(array7)
    if size1 == min(size1,size2,size3,size4,size5,size6,size7):
        return array1
    if size2 == min(size1,size2,size3,size4,size5,size6,size7):
        return array2
    if size3 == min(size1,size2,size3,size4,size5,size6,size7):
        return array3
    if size4 == min(size1,size2,size3,size4,size5,size6,size7):
        return array4
    if size5 == min(size1,size2,size3,size4,size5,size6,size7):
        return array5
    if size6 == min(size1,size2,size3,size4,size5,size6,size7):
        return array6
    else:
        return array7