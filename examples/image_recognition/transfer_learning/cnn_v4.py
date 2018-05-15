import sys

sys.path.append('..')
from loader import load_data_transfer_learning as loader

import numpy as np
import time
from vgg16 import VGG16
from imagenet_utils import decode_predictions
from keras.layers import Dense, Activation, Flatten
from keras.layers import merge, Input
from keras.models import Model
from keras.utils import np_utils
from sklearn.cross_validation import train_test_split


x, y, labels = loader("../fruits-360/Validation")
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2,
                                                    random_state=2)


num_classes = len(labels)
# convert class labels to on-hot encoding
y_train = np_utils.to_categorical(Y_train, len(labels))
y_test = np_utils.to_categorical(Y_test, len(labels))


names = labels

#########################################################################################
# Custom_vgg_model_1
# Training the classifier alone
image_input = Input(shape=(224, 224, 3))

model = VGG16(input_tensor=image_input, include_top=True, weights='imagenet')
last_layer = model.get_layer('fc2').output
out = Dense(num_classes, activation='softmax', name='output')(last_layer)
custom_vgg_model = Model(image_input, out)
custom_vgg_model.summary()

for layer in custom_vgg_model.layers[:-1]:
    layer.trainable = False

custom_vgg_model.compile(loss='categorical_crossentropy', optimizer='rmsprop',
                         metrics=['accuracy'])

hist = custom_vgg_model.fit(X_train, y_train, batch_size=32, epochs=12,
                            verbose=1, validation_data=(X_test, y_test))
(loss, accuracy) = custom_vgg_model.evaluate(X_test, y_test, batch_size=10,
                                             verbose=1)

print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss, accuracy * 100))
custom_vgg_model.save("cnn_tl_v4.h5")

