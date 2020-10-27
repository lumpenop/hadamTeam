import numpy as np
import cv2
from matplotlib import pyplot as plt
# %matplotlib inline

image = cv2.imread('../images/bong.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

xml = '../data/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)
faces = face_cascade.detectMultiScale(gray, 1.2, 5)

print("Number of faces detected: " + str(len(faces)))

if len(faces):
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), cmap='gray')
plt.xticks([]), plt.yticks([]) 
plt.show()

