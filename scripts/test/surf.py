import cv2
import numpy as np

img = cv2.imread('/home/roper/hackatum/train/10106-brHD/logo1-0/10106_2017-11-08_07.55.47_5.jpg')


# Create SURF object. You can specify params here or later.
# Here I set Hessian Threshold to 400
surf = cv2.xfeatures2d.SURF_create(400)

# Find keypoints and descriptors directly
kp, des = surf.detectAndCompute(img,None)



kp = surf.detect(img,None)
img2 = cv2.drawKeypoints(img,kp,None,(255,0,0),4)

plt.imshow(img2),plt.show()