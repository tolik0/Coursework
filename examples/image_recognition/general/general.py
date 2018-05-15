import keras
from PIL import Image
import numpy

names = ['Apple Braeburn',
         'Apple Golden 1',
         'Apple Golden 2',
         'Apple Golden 3',
         'Apple Granny Smith',
         'Apple Red 1',
         'Apple Red 2',
         'Apple Red 3',
         'Apple Red Delicious',
         'Apple Red Yellow',
         'Apricot',
         'Avocado',
         'Avocado ripe',
         'Banana',
         'Banana Red',
         'Cactus fruit',
         'Carambula',
         'Cherry',
         'Clementine',
         'Cocos',
         'Dates',
         'Granadilla',
         'Grape Pink',
         'Grape White',
         'Grape White 2',
         'Grapefruit Pink',
         'Grapefruit White',
         'Guava',
         'Huckleberry',
         'Kaki',
         'Kiwi',
         'Kumquats',
         'Lemon',
         'Lemon Meyer',
         'Limes',
         'Litchi',
         'Mandarine',
         'Mango',
         'Maracuja',
         'Nectarine',
         'Orange',
         'Papaya',
         'Passion Fruit',
         'Peach',
         'Peach Flat',
         'Pear',
         'Pear Abate',
         'Pear Monster',
         'Pear Williams',
         'Pepino',
         'Pineapple',
         'Pitahaya Red',
         'Plum',
         'Pomegranate',
         'Quince',
         'Raspberry',
         'Salak',
         'Strawberry',
         'Tamarillo',
         'Tangelo']

model = keras.models.load_model("cnn_v3.h5")

img = Image.open("../test_images/banan.jpg")
img = img.resize((64, 64))
image = numpy.array(img)
X = []
X.append(image)
X = numpy.array(X)

classes = model.predict(X)

print(classes)
