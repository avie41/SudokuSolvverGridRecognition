from PIL import Image
import torch, torchvision
import numpy as np
import os

# Get list of images in Cases/ folder
# list_folders = os.listdir('Cases/')

# Treating images
def img_ML(path):
    """
    Changing the image to an input for the pytorch model
    """
    img = Image.open(path)
    # Black and White
    img = img.convert('L')
    img = np.array(img.getdata())
    img = img/255

    # kernel = np.ones((3,3),np.uint8)
    # erosion = cv2.erode(dst,kernel,iterations = 1)

    # Sets white values as -1
    img[img>0.4] = -1.0
    # Set others at 0
    img[img>-1] = 0
    img = np.array([img])
    # Transforms image to tensor
    img = torchvision.transforms.ToTensor()(img)
    img = img.type(torch.FloatTensor).view(1, 784)

    return img

# Loading model
# model = torch.load('model.pt')
# model.eval

# Take an image
# img = img_ML('28img.png')

def predict(model, img):
    with torch.no_grad():
        logps = model(img)

    ps = torch.exp(logps)
    probab = list(ps.numpy()[0])
    return probab.index(max(probab)), max(probab)

# print(predict(img))
# grid = [[0 for i in range(9)] for i in range(9)]
# for p in list_folders:    
#     img = Image.open('Cases/' + p)
#     img = img.resize((28,28), Image.ANTIALIAS)
#     img.save('Cases/' + p)

#     img = img_ML('Cases/' + p)

#     nb = predict(img)

#     grid[int(p[3])][int(p[4])] = nb
#     print(nb)

# print(grid)
