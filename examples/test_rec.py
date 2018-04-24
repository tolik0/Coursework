# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import os
from PIL import Image
from loader import load_data
from test_cv2 import find_green_object
import cv2


X_train, y_train, labels = load_data("../fruits-360/Training")
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_train, y_train)
image = find_green_object("apple1.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = Image.fromarray(image, 'RGB')
image = image.resize((30, 30))
image = np.array(image)
image = image.flatten()
res = model.predict(image.reshape(1, -1))
print("This is - {}".format(labels[int(res)]))