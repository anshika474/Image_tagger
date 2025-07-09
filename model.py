
import torch
from torchvision import models, transforms
from PIL import Image
import urllib.request
import os

# Load model once
model = models.mobilenet_v2(pretrained=True)
model.eval()

# ImageNet preprocessing
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Download and load labels once
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
LABELS_FILE = "imagenet_classes.txt"

if not os.path.exists(LABELS_FILE):
    urllib.request.urlretrieve(LABELS_URL, LABELS_FILE)

with open(LABELS_FILE, "r") as f:
    categories = [s.strip() for s in f.readlines()]

# Prediction function
def get_predictions(image_path):
    image = Image.open(image_path).convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

    top3_prob, top3_catid = torch.topk(probabilities, 3)
    return [categories[catid] for catid in top3_catid]



