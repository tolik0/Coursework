import numpy as np
import os
from PIL import Image

path = "../fruits-360/Validation/Apple Braeburn"
filename = "1.jpg"
image = Image.open(os.path.join(path, filename))
image1 = image
width = image.width
height = image.height
image = np.array(image)
image = list(image.flatten())
print(len(image), width, height)
porig = sum(image) / len(image)
res = set()
print(width, height, porig, len(image))
for i in range(len(image)):
    if image[i] < porig:
        res.add((i // (3 * width), (i % (3 * width)) // 3))
max_height = max(res, key = lambda x: x[0])[0]
min_height = min(res, key = lambda x: x[0])[0]
max_width = max(res, key = lambda x: x[1])[1]
min_width = min(res, key = lambda x: x[1])[1]
area = (min_width, min_height, max_width, max_height)
print(area)
cropped_img = image1.crop(area)
cropped_img.save("2.jpg")
