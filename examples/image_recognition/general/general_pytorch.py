import torch
from torchvision import transforms
from torch.autograd import Variable
from PIL import Image

import sys
sys.path.append('../object_detection')
from image_detector import find_objects

images = find_objects("../test_images/ban_app.jpg")

for i in range(len(images)):
    cv2.imshow(f"{i}", images[i])
cv2.waitKey(0)

model_path = ""
image_path = ""
model = torch.load(model_path)

loader = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name)
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    return image.cuda()  #assumes that you're using GPU

image = image_loader(image_path)

print(model(image))
