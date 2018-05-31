import numpy as np
import cv2


def crop_minAreaRect(img, rect):
    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
               pts[1][0]:pts[2][0]]

    return img_crop


def find_objects(path):
    boundaries = [(np.array([10, 10, 10]), np.array([28, 255, 255])), #yellow
                  (np.array([28, 10, 10]), np.array([80, 255, 255])), #green
                  (np.array([0, 10, 10]), np.array([10, 255, 255]))] #red


    image = cv2.imread(path)
    bordersize = 50
    image = cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize,
                                left=bordersize, right=bordersize,
                                borderType=cv2.BORDER_CONSTANT,
                                value=[255, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    images = []

    for (lower, upper) in boundaries:
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(image, image, mask=mask)

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)
        index = []

        for i in range(len(contours)):
            if len(contours[i]) < 100:
                index.append(i)

        contours = np.delete(contours, index)

        for contour in contours:
            rect = cv2.minAreaRect(contour)

            # image1 = image.copy()
            # box = cv2.boxPoints(rect)
            # box = np.int0(box)
            # cv2.drawContours(image1, [box], 0, (0, 0, 255), 2)
            # cv2.imshow('image', image1)
            # cv2.waitKey(0)

            img = crop_minAreaRect(image, rect)
            img[np.where((img == [0, 0, 0]).all(axis=2))] = [255, 255, 255]
            images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    return images


if __name__ == "__main__":
    images = find_objects("ban_app.jpg")
    for i in range(len(images)):
        cv2.imshow(f"{i}", images[i])
    cv2.waitKey(0)
