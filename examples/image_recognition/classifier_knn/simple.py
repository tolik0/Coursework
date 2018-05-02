# import the necessary packages
from sklearn.neighbors import KNeighborsClassifier
from examples.image_recognition.loader import load_data

X_train, y_train, labels = load_data("../fruits-360/Training")
X_test, y_test, labels = load_data("../fruits-360/Validation")
for k in range(1, 50):
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print("For k = {} - score is {}".format(k, score))
