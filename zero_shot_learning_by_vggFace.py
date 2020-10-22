import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import glob
from PIL import Image


class VGG_16(nn.Module):
    def __init__(self):
        super().__init__()
        self.block_size = [2, 2, 3, 3, 3]
        self.conv1_1 = nn.Conv2d(3, 64, 3, stride=1, padding=1)
        self.conv1_2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.conv2_1 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
        self.conv2_2 = nn.Conv2d(128, 128, 3, stride=1, padding=1)
        self.conv3_1 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
        self.conv3_2 = nn.Conv2d(256, 256, 3, stride=1, padding=1)
        self.conv3_3 = nn.Conv2d(256, 256, 3, stride=1, padding=1)
        self.conv4_1 = nn.Conv2d(256, 512, 3, stride=1, padding=1)
        self.conv4_2 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.conv4_3 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.conv5_1 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.conv5_2 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.conv5_3 = nn.Conv2d(512, 512, 3, stride=1, padding=1)
        self.fc6 = nn.Linear(512 * 7 * 7, 4096)
        self.fc7 = nn.Linear(4096, 4096)
        self.fc8 = nn.Linear(4096, 2622)

    def forward(self, x):
        """ Pytorch forward
        Args:
            x: input image (224x224)
        Returns: class logits
        """
        x = F.relu(self.conv1_1(x))
        x = F.relu(self.conv1_2(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2_1(x))
        x = F.relu(self.conv2_2(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv3_1(x))
        x = F.relu(self.conv3_2(x))
        x = F.relu(self.conv3_3(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv4_1(x))
        x = F.relu(self.conv4_2(x))
        x = F.relu(self.conv4_3(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv5_1(x))
        x = F.relu(self.conv5_2(x))
        x = F.relu(self.conv5_3(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc6(x))
        x = F.dropout(x, 0.5, self.training)
        x = self.fc7(x)
        # x = F.dropout(x, 0.5, self.training)
        # x = self.fc8(x)
        return x


class Network():
    def __init__(self, load_path = None):
        self.cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.cuda else "cpu")
        print("Classifier running on GPU" if self.cuda else "Classifier running on CPU")
        self.model = VGG_16().to(self.device)
        if load_path!=None:
            self.model.load_state_dict(torch.load(load_path))
        self.loss_f = nn.L1Loss()

    def predict(self, im1, im2):
        self.model.eval()
        with torch.no_grad():
            output1 = self.model(self.preprocess_image(im1).unsqueeze(0))
            output2 = self.model(self.preprocess_image(im2).unsqueeze(0))
        return self.loss_f(output1,output2)

    def preprocess_image(self, img):
        img = img.resize((224, 224), Image.ANTIALIAS)
        try:
            img = np.array([img.getdata(0),img.getdata(1),img.getdata(2)])
        except:
            img = np.array([img.getdata(0),img.getdata(0),img.getdata(0)])
        
        img = torch.tensor(img.reshape(3,224,224)).float().to(self.device)
        return img

classifier = Network('/data/sba/khy_project/pretrained/vgg_face_dag.pth')

results = []
for pred_file in glob.glob("/data/sba/khy_project/clean_test/*"):
    im1 = Image.open(pred_file)
    mini = 10000
    predict = None
    for file in glob.glob("/data/sba/khy_project/clean_class/*"):
        try:
            im2 = Image.open(file)
            score = classifier.predict(im1,im2)
            if score < mini:
                mini = score
                predict = file.split('/')[-1].split('.')[0]
        except:
            pass
    results.append([pred_file.split('/')[-1], predict])

results

count = 0
for result in results:
  if result[0].startswith(result[1]):
    count += 1
print('Acc : %0.4f %%' %(100*count/len(results)))