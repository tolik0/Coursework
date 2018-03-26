# import the necessary packages
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from loader import load_data

X, y, labels = load_data("../fruits-360/Training")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(score)