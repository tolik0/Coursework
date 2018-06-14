import torch
from torchvision import transforms
from torch.autograd import Variable
from PIL import Image
import cv2
import numpy as np


def detector(model, image_path, to_image_url):
    names = ['acerolas',
             'apples',
             'apricots',
             'avocados',
             'bananas',
             'blackberries',
             'blueberries',
             'cantaloupes',
             'cherries',
             'coconuts',
             'figs',
             'garbage',
             'grapefruits',
             'grapes',
             'guava',
             'kiwifruit',
             'lemons',
             'limes',
             'mangos',
             'olives',
             'oranges',
             'passionfruit',
             'peaches',
             'pears',
             'pineapples',
             'plums',
             'pomegranates',
             'raspberries',
             'strawberries',
             'tomatoes',
             'watermelons']

    loader = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

    def image_loader(image):
        """load image, returns cuda tensor"""
        image = loader(image).float()
        image = Variable(image, requires_grad=True)
        image = image.unsqueeze(
            0)  # this is for VGG, may not be needed for ResNet
        return image.cuda()  # assumes that you're using GPU

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
        ingr = []
        boundaries = [(np.array([0, 0, 0]), np.array([179, 255, 20])),
                      # black
                      (np.array([10, 10, 10]), np.array([18, 255, 255])),
                      # orange
                      (np.array([18, 10, 10]), np.array([28, 255, 255])),
                      # yellow
                      (np.array([28, 10, 10]), np.array([85, 255, 255])),
                      # green
                      (np.array([85, 10, 10]), np.array([140, 255, 255])),
                      # blue
                      (np.array([140, 10, 10]), np.array([160, 255, 255])),
                      # pink
                      ((np.array([160, 10, 10]), np.array([179, 255, 255])),
                       # red
                       (np.array([0, 10, 10]), np.array([13, 255, 255])))]

        image = cv2.imread(path)
        image_size = image.shape[0] * image.shape[1]
        bordersize = int(0.2 * np.sqrt(image_size))
        image = cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize,
                                   left=bordersize, right=bordersize,
                                   borderType=cv2.BORDER_CONSTANT,
                                   value=[255, 255, 255])

        image1 = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        images = []

        for (lower, upper) in boundaries:
            if type(lower) == tuple:
                mask1 = cv2.inRange(hsv, lower[0], lower[1])
                mask2 = cv2.inRange(hsv, upper[0], upper[1])
                mask = mask1 | mask2
                print(0)
            else:
                mask = cv2.inRange(hsv, lower, upper)
            im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                                        cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                rect = cv2.minAreaRect(contour)

                box = cv2.boxPoints(rect)
                box = np.int0(box)

                size = np.sqrt((box[0][0] - box[1][0]) ** 2 +
                               (box[0][1] - box[1][1]) ** 2) * \
                       np.sqrt((box[1][1] - box[2][1]) ** 2 +
                               (box[1][0] - box[2][0]) ** 2)

                if size < 0.05 * image_size:
                    continue

                startX, startY = min(box, key=lambda x: x[0])[0], \
                                 min(box, key=lambda x: x[1])[1]

                # display the prediction
                img = crop_minAreaRect(image, rect)
                croped_image = image_loader(
                    Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
                outputs = \
                    torch.nn.Softmax()(model(croped_image)).data.cpu().numpy()[
                        0]

                ind = outputs.argsort()[-3:][::-1]
                ind_max = outputs.argsort()[-1:][::-1]
                if names[ind[0]] != 'garbage1':
                    cv2.drawContours(image1, [box], 0, (0, 0, 255), 2)
                    label = ""
                    for i in ind:
                        label += "  {}: {}%".format(names[i],
                                                    round(outputs[i] * 100,
                                                          1)) + "\n"

                    for i in ind_max:
                        ingr.append(names[i])

                    y, dy = startY, 15
                    for line in label.split('\n'):
                        y += dy
                        # cv2.putText(image1, line, (startX, y),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)

                    img[np.where((img == [0, 0, 0]).all(axis=2))] = [255, 255,
                                                                     255]
                    images.append(img)

        return cv2.cvtColor(image1, cv2.COLOR_BGR2RGB), ingr

    img, ingr = find_objects(image_path)

    Image.fromarray(img).save("images/" + to_image_url)
    print(ingr)
    ingr = list(set(ingr))
    return ingr


if __name__ == "__main__":
    model_path = "mymodel_finetuning_new_v1.pth"
    model = torch.load(model_path)
    detector(model, "test_images/banan.jpg")
