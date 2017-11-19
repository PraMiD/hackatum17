import numpy as np
from scipy import ndimage, stats

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
    UPDATED
    """
    return (np.sum(array, axis = 2)/3.0).astype(np.int)

def color_to_single_color(array, color):
    """
    Converst a colored image to a black and white image of a specific color.
    #color -> 0 == red; 1 == green; 2 == blue
    UPDATED
    """
    return array[:,:,color]

def color_to_dual_color(array, color1, color2):
    """
    Converst a colored image to a black and white image of two specific colors.
        #color -> 0 == red; 1 == green; 2 == blue
    UPDATED
    """
    return ((array[:,:,color1] + array[:,:,color1])/2.0).astype(np.int)

def apply_filter(array, filter_):
    """
    Applies a symmetric (3x3, 5x5, etc.) filter to the array.
    UPDATED
    """
    return ndimage.convolve(array, filter_, mode='constant', cval=0.0)

def pythagoras_dual(array1, array2):
    """
    Calculates the length of the hypothenuses to each pixels x and y values.
    UPDATED
    """
    return np.linalg.norm(np.array([zip(x, y) for x, y in zip(array1, array2)]), axis=2)

def pythagoras_single(array):
    """
    Calculates the length of the hypothenuses to each pixels x and y values.
    UPDATED
    """
    return np.linalg.norm(array, axis=2)

def max_bw(array, value = 255):
    """
    Scales an array so that the highest pixel value is equal to the parameter value.
    UPDATED
    """
    m = np.max(array)
    c = value
    width = len(array[0])
    height = len(array)
    array /= float(m)
    array *= value
    return array.astype(np.int)

def darken(array, amount = 0.7):
    """
    Reduces the values of a matrix by a percentage (amount, e.g. 0.4 -> 40%) of the brightest pixel.
    UPDATED
    """
    m = amount * np.max(array)
    return np.where(array > m, array, 0)

def threshold(array, value):
    """
    Applies a threshold to the array, that sets every pixel which value is less
    that the paramenter value to 0. All the other pixels keep their values.
    """
    return stats.threshold(array, threshmin=value, newval=0)

def solo_edge(array):
    """
    Reduces all Edges to 1 pixel in width.
    NOT NECESSARY
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

def edge_approach(array, noise = 0.4):
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

    return (array[top:(height-bottom),left:(width-right)],top,bottom,left,right)

def symmetric_canny(array):
    arrayh = apply_filter(array,canny_filter_horizontal)
    arrayv = apply_filter(array,canny_filter_vertical)
    return (pythagoras_dual(arrayh,arrayv))

def array_size(array):
    return (len(array) * len(array[0]))

def my_canny(array):
    array1 = edge_approach(max_bw(symmetric_canny(darken(color_to_single_color(array,0)))))
    array2 = edge_approach(max_bw(symmetric_canny(darken(color_to_single_color(array,1)))))
    array3 = edge_approach(max_bw(symmetric_canny(darken(color_to_single_color(array,2)))))
    array4 = edge_approach(max_bw(symmetric_canny(darken(color_to_dual_color(array,0,1)))))
    array5 = edge_approach(max_bw(symmetric_canny(darken(color_to_dual_color(array,1,2)))))
    array6 = edge_approach(max_bw(symmetric_canny(darken(color_to_dual_color(array,0,2)))))
    array7 = edge_approach(max_bw(symmetric_canny(darken(color_to_bw(array)))))
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

def my_canny_h(array):
    array1 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array,0)),canny_filter_horizontal)))
    array2 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array,0)),canny_filter_horizontal)))
    array3 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array,0)),canny_filter_horizontal)))
    array4 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array,0,1)),canny_filter_horizontal)))
    array5 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array,1,2)),canny_filter_horizontal)))
    array6 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array,0,2)),canny_filter_horizontal)))
    array7 = edge_approach(max_bw(apply_filter(darken(color_to_bw(array)),canny_filter_horizontal)))
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

def my_canny_v(array):
    array1 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array, 0)), canny_filter_vertical)))
    array2 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array, 0)), canny_filter_vertical)))
    array3 = edge_approach(max_bw(apply_filter(darken(color_to_single_color(array, 0)), canny_filter_vertical)))
    array4 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array, 0, 1)), canny_filter_vertical)))
    array5 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array, 1, 2)), canny_filter_vertical)))
    array6 = edge_approach(max_bw(apply_filter(darken(color_to_dual_color(array, 0, 2)), canny_filter_vertical)))
    array7 = edge_approach(max_bw(apply_filter(darken(color_to_bw(array)), canny_filter_vertical)))
    size1 = array_size(array1)
    size2 = array_size(array2)
    size3 = array_size(array3)
    size4 = array_size(array4)
    size5 = array_size(array5)
    size6 = array_size(array6)
    size7 = array_size(array7)
    if size1 == min(size1, size2, size3, size4, size5, size6, size7):
        return array1
    if size2 == min(size1, size2, size3, size4, size5, size6, size7):
        return array2
    if size3 == min(size1, size2, size3, size4, size5, size6, size7):
        return array3
    if size4 == min(size1, size2, size3, size4, size5, size6, size7):
        return array4
    if size5 == min(size1, size2, size3, size4, size5, size6, size7):
        return array5
    if size6 == min(size1, size2, size3, size4, size5, size6, size7):
        return array6
    else:
        return array7

def edge_approach_02(array, noise = 0.4):
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

    return (top,bottom,left,right)

def cut_size((y0,y1,x0,x1)):
    return ((y1 - y0) * (x1 - x0))

def my_canny_02(array):
    array1 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_single_color(array,0)))))
    array2 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_single_color(array,1)))))
    array3 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_single_color(array,2)))))
    array4 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_dual_color(array,0,1)))))
    array5 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_dual_color(array,1,2)))))
    array6 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_dual_color(array,0,2)))))
    array7 = edgeApproach02(maxBw(symmetric_canny(darken(color_to_bw(array)))))
    size1 = cut_size(array1)
    size2 = cut_size(array2)
    size3 = cut_size(array3)
    size4 = cut_size(array4)
    size5 = cut_size(array5)
    size6 = cut_size(array6)
    size7 = cut_size(array7)
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

def my_canny_03(array):
    return edge_approach(max_bw(symmetric_canny(darken(color_to_bw(array)))))

def my_canny_04(array):
    return max_bw(symmetric_canny(darken(color_to_bw(array))))

def cut_corner(array, corner, a = 0.2):
    cuts = np.array([[0.0,a,0.0,a],[0.0,a,1.0-a,1.0],[1.0-a,1.0,0.0,a],[1.0-a,1.0,1.0-a,1.0]])
    width = len(array[0])
    height = len(array)
    cutx = (cuts[corner][2:] * width).astype(dtype = np.int)
    cuty = (cuts[corner][:2] * height).astype(dtype = np.int)
    return array[cuty[0]:cuty[1],cutx[0]:cutx[1]]
