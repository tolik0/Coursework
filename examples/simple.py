# import the necessary packages
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn import datasets
from skimage import exposure
import numpy as np

mnist = datasets.load_digits()

X_train, X_test, y_train, y_test = train_test_split(mnist.data, mnist.target, test_size=0.1, random_state=42)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(score)
"""
import numpy as np
import PIL
img = np.array(PIL.Image.open('test.jpg'))
img = np.reshape(img, 151200)
"""
