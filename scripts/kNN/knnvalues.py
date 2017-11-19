import numpy as np
import math
from PIL import Image
import os
import pickle

def get_features(array):
    width = len(array[0])
    height = len(array)
    mean = np.mean(array)
    std = np.std(array)
    return [width, height, mean, std]

features_ = []

path_nologo = "%s/data/nologo_train" % os.getcwd()
path_logo = "%s/data/" % os.getcwd()

folders_logo = os.listdir(path_logo)
folders_logo = [x for x in folders_logo if ((x.endswith('train') and not x.startswith('.')))]

for i in folders_logo:
    logo_paths = os.listdir("%s/%s" % (path_logo, i))
    logo_paths = [x for x in logo_paths if not x.startswith('.')]
    for j in logo_paths:
        path_logo_image = "%s/%s/%s" % (path_logo, i, j)
        pic = Image.open(path_logo_image)
        array = np.asarray(pic)
        features_.append([get_features(array),1])

nologo_path = os.listdir(path_nologo)
nologo_path = [x for x in nologo_path if not x.startswith('.') and x.endswith('.png')]

for j in nologo_path:
    path_nologo_image = "%s/%s" % (path_nologo, j)
    pic = Image.open(path_nologo_image)
    array = np.asarray(pic)
    features_.append([get_features(array),0])

def knn(test, features_, k=5):
    distances = []
    for e in features_:
        distances.append([np.linalg.norm(e[0] - np.array(test)), e[1]])
    distances.sort()
    sum = 0
    for i in range(k):
        sum += distances[0][1]
    return (0 if sum <= 4 else 1)

def use_knn(path, features_):
    pic = Image.open(path)
    array = np.asarray(pic)
    return knn(features(array), features_)

def test_knn():
    logo_count = 0
    correct = 0
    folders_logo = os.listdir(path_logo)
    folders_logo = [x for x in folders_logo if ((x.endswith('test') and not x.startswith('.')))]

    for i in folders_logo:
        logo_paths = os.listdir("%s/%s" % (path_logo, i))
        logo_paths = [x for x in logo_paths if not x.startswith('.')]
        for j in logo_paths[:11]:
            logo_count += 1
            path_logo_image = "%s/%s/%s" % (path_logo, i, j)
            pic = Image.open(path_logo_image)
            array = np.asarray(pic)
            correct += 1 if (knn(get_features(array), features_) == 1) else 0

    print "Logo Detection accuracy: %f" % (correct/float(logo_count))

    nologo_count = 0
    correct = 0
    nologo_paths = os.listdir(path_nologo)
    nologo_paths = [x for x in nologo_paths if ((x.endswith('test') and not x.startswith('.')))]

    for j in logo_paths[:100]:
        nologo_count += 1
        path_nologo_image = "%s/%s" % (path_nologo, j)
        pic = Image.open(path_nologo_image)
        array = np.asarray(pic)
        correct += 1 if (knn(get_features(array), features_) == 0) else 0

    print "Nologo Detection accuracy: %f" % (correct / float(nologo_count))

test_knn()