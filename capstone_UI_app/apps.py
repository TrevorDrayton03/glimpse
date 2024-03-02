from django.apps import AppConfig
from ultralytics import YOLO
import torch
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
        CapstoneUiAppConfig.model = YOLO('capstone_UI_app/best.pt')

# resnet 18 model
def initialize_and_predict(image_path):
    # Function to load and preprocess the image
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