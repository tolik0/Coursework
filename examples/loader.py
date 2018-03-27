import numpy as np
import os
from PIL import Image


def load_data(train_path, valid_path):
    """
    TODO: Add documentation
    :param path:
    :return:
    """
    labels = []
    X = []
    y = []
    products = os.listdir(train_path)
    for i, product in enumerate(products):
        print("Product {} [{}/{}] loaded...".format(product, i + 1,
                                                    len(products)))
        labels.append(product)
        for path in (train_path, valid_path):
            images = os.listdir(os.path.join(path, product))
            for filename in images:
                image = np.array(Image.open(os.path.join(path, product,
                                                         filename)))
                image.resize((25, 25))
                image = image.flatten()
                X.append(image)
                y.append(i)

    X = np.array(X)
    y = np.array(y)
    return X, y, labels


if __name__ == "__main__":
    X, y, labels = load_data("../fruits-360/Validation")
    print(X.shape)
    print(y.shape)
    print(labels)
