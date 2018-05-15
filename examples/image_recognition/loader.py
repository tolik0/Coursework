import numpy as np
import os
from PIL import Image
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input


def load_data(path):
    """
    TODO: Add documentation
    :param path:
    :return:
    """
    labels = []
    X = []
    y = []
    products = os.listdir(path)
    for i, product in enumerate(products):
        print("Product {} [{}/{}] loaded...".format(product, i + 1,
                                                    len(products)))
        labels.append(product)
        images = os.listdir(os.path.join(path, product))
        for filename in images:
            img = Image.open(os.path.join(path, product, filename))
            img.thumbnail((50, 50), Image.ANTIALIAS)
            image = np.array(img)
            image = image.flatten()
            X.append(image)
            y.append(i)

    X = np.array(X)
    y = np.array(y)
    return X, y, labels


def load_data_convolutional(path):
    """
    TODO: Add documentation
    :param path:
    :return:
    """
    labels = []
    X = []
    y = []
    products = os.listdir(path)
    for i, product in enumerate(products):
        print("Product {} [{}/{}] loaded...".format(product, i + 1,
                                                    len(products)))
        labels.append(product)
        images = os.listdir(os.path.join(path, product))
        for filename in images:
            img = Image.open(os.path.join(path, product, filename))
            img.thumbnail((64, 64), Image.ANTIALIAS)
            image = np.array(img)
            X.append(image)
            y.append(i)

    X = np.array(X)
    y = np.array(y)
    return X, y, labels


def load_data_transfer_learning(path):
    """
    TODO: Add documentation
    :param path:
    :return:
    """
    labels = []
    X = []
    y = []
    products = os.listdir(path)
    for i, product in enumerate(products):
        print("Product {} [{}/{}] loaded...".format(product, i + 1,
                                                    len(products)))
        labels.append(product)
        images = os.listdir(os.path.join(path, product))
        for filename in images:
            img = image.load_img(os.path.join(path, product, filename),
                                 target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            X.append(x)
            y.append(i)

    X = np.array(X)
    y = np.array(y)

    X = np.rollaxis(X, 1, 0)
    X = X[0]
    return X, y, labels


if __name__ == "__main__":
    X, y, labels = load_data("../fruits-360/Validation")
    print(X.shape)
    print(y.shape)
    print(labels)
