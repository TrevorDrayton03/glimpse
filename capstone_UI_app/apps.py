from django.apps import AppConfig
from ultralytics import YOLO
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from torch.autograd import Variable
from torchvision import models, transforms
import torch
from PIL import Image
from torch.autograd import Variable

class CapstoneUiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capstone_UI_app'
    
    model = None
    
    def ready(self):
        CapstoneUiAppConfig.model = YOLO('capstone_UI_app/yolov8_model.pt')

def load_and_preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = Variable(image.unsqueeze(0))
    
    return image    

# resnet 18 model
def resnet_initialize_and_predict(image_path):
    # Initialize ResNet-18 model
    model = models.resnet18(pretrained=False)  # Set pretrained=True if you want to use a model pre-trained on ImageNet
    model.fc = torch.nn.Linear(512, 2)  # Adjust the number of classes based on your model
    # Load the model weights
    model_weights_path = 'capstone_UI_app/resnet18_model.pth'
    model.load_state_dict(torch.load(model_weights_path, map_location=torch.device('cpu')))
    model.eval()

    # Load and preprocess the input image
    input_image = load_and_preprocess_image(image_path)

    # Forward pass to get predictions
    with torch.no_grad():
        output = model(input_image)

    # Get predicted class and probabilities
    predicted_class = torch.argmax(output, dim=1).item()
    probabilities = torch.nn.functional.softmax(output, dim=1).squeeze().tolist()

    return predicted_class, probabilities


# def vgg_initialize_and_predict(image_path):
#     # Initialize VGG-16 model with pretrained weights
#     model = models.vgg16(pretrained=False)  # Set pretrained=True if you want to use pre-trained weights

#     # Replace the final fully connected layer
#     model.classifier._modules['6'] = nn.Linear(4096, 2)  # Adjust the number of output nodes based on your task

#     # Load the state dictionary
#     model_weights_path = 'capstone_UI_app/vgg16_model.pth'
#     state_dict = torch.load(model_weights_path, map_location=torch.device('cpu'))

#     # Adjust state dictionary to match model architecture and resize mismatched parameters
#     new_state_dict = {}
#     for key, value in state_dict.items():
#         if key.startswith('features') or key.startswith('classifier'):
#             new_key = key.replace('module.', '')  # Remove 'module.' prefix if present
#             if new_key in model.state_dict():
#                 if 'features.19' in key:  # Resize features.19.weight
#                     # Check if resizing is needed
#                     if len(value.shape) > 1 and value.shape[1] != 512:
#                         # Resize from [512, 256, 3, 3] to [512, 512, 3, 3]
#                         value = value.repeat(1, 2, 1, 1)
#                 new_state_dict[new_key] = value

#     # # Load the adjusted state dictionary into the model
#     model.load_state_dict(new_state_dict, strict=False)  # Set strict=False to allow for missing keys
#     # model.load_state_dict(state_dict, strict=False)
#     model.eval()

#     # Load and preprocess the input image
#     input_image = Image.open(image_path)
#     preprocess = transforms.Compose([
#         transforms.Resize(256),
#         transforms.CenterCrop(224),
#         transforms.ToTensor(),
#         transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#     ])
#     input_tensor = preprocess(input_image)
#     input_batch = input_tensor.unsqueeze(0)  # Add a batch dimension

#     # Forward pass to get predictions
#     with torch.no_grad():
#         output = model(input_batch)

#     # Get predicted class and probabilities
#     predicted_class = torch.argmax(output, dim=1).item()
#     probabilities = torch.nn.functional.softmax(output, dim=1).squeeze().tolist()

#     return predicted_class, probabilities