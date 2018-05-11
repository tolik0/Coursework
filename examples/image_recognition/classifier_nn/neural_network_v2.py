import sys
sys.path.append('..')
from loader import load_data

import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
import pandas
import pickle
from PIL import Image
from keras import backend as K
print(K.tensorflow_backend._get_available_gpus())

seed = 7
numpy.random.seed(seed)

X_train, Y_train, labels = load_data("../fruits-360/Training")
X_test, Y_test, labels = load_data("../fruits-360/Validation")
X_train, X_test = X_train / 255, X_test / 255

encoder = LabelEncoder()
encoder.fit(Y_train)
encoded_Y_train = encoder.transform(Y_train)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y_train = np_utils.to_categorical(encoded_Y_train)


encoder = LabelEncoder()
encoder.fit(Y_test)
encoded_Y_test = encoder.transform(Y_test)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y_test = np_utils.to_categorical(encoded_Y_test)


# define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(256, input_dim=7500, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(60, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


model = baseline_model()

model.fit(X_train, dummy_y_train, epochs=20, batch_size=128)

loss_and_metrics = model.evaluate(X_test, dummy_y_test, batch_size=128)

print(loss_and_metrics)


X = []
img = Image.open("banan.jpg")
img = img.resize((50, 50))
image = numpy.array(img)
image = image.flatten()
X.append(image)
X = numpy.array(X)

classes = model.predict(X)

print(classes)


with open('pickled_neural', 'wb') as file:
    pickle.dump(model, file)


# In[ ]:


from sklearn.model_selection import permutation_test_score

