from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
from PIL import Image

import torch.nn as nn
from torch import load
from torchvision import transforms, models

class ImageTransform():
    def __init__(self, resize, mean, std):
        self.data_transform = {
            'val': transforms.Compose([
                transforms.Resize(resize),  # リサイズ
                transforms.ToTensor(),  # テンソルに変換
                transforms.Normalize(mean, std)  # 標準化
            ])
        }

    def __call__(self, img, phase='val'):
        return self.data_transform[phase](img)

class Model():
    def __init__(self, weight):
        self.net = models.vgg16(True)
        self.net.classifier[6] = nn.Linear(in_features=4096, out_features=10)
        self.net.eval()
        net_weights = load(weight,map_location={'cuda:0': 'cpu'})
        self.net.load_state_dict(net_weights)

    def call(self,Input):
        return self.net(Input)

def  Plt_to_Pil(i,j):
    fig = plt.figure(figsize=(6,6), dpi=50)
    ax = fig.add_subplot(1, 1, 1)
    ax.axis('off')
    ax.plot(i,j,'k')
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    fig.clf()
    return Image.fromarray(img).convert('RGB')