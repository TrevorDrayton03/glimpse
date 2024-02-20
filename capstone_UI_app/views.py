from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ContactForm, BillingForm, RegisterForm, ImageUploadForm
from .models import UploadedImage
from django.contrib import messages

# python libraries for preprocessing
import cv2
import numpy as np
from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps
import base64
from urllib.parse import urljoin
from skimage import exposure


def main_view(request):
    if request.GET.get('ajax') == '1':
        # If it's an AJAX request, return the AJAX template
        return render(request, 'ajax_main.html')
    else:
        return render(request, 'main.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            # get the data from the form
            company_name = form.cleaned_data.get('company_name')
            # then use the valid data
            ###
            return redirect('billing')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def billing_view(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            return redirect('thankyou')
    else:
        form = BillingForm()

    return render(request, 'contact.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            # return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def thankyou_view(request):
    return render(request, 'thankyou.html')

@login_required(login_url='/')
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/')
def custom_logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            error_message = 'Invalid login credentials'
            return JsonResponse({'error': error_message})

    return render(request, 'dashboard.html') 

# LoginView automatically handles the authentication process
class custom_login_view(LoginView):
    template_name = 'login.html' 
    redirect_authenticated_user = True # defined in settings.py as LOGIN_REDIRECT_URL

@login_required(login_url='/')
def dashboard_upload_view(request):
    all_images = UploadedImage.objects.all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            new_image = UploadedImage(image=uploaded_image)
            new_image.save()
    else:
        form = ImageUploadForm()

    context = {'form': form, 'images': all_images if all_images.exists() else []}

    return render(request, 'dashboard_upload.html', context)

@login_required(login_url='/')
def dashboard_upload_edit_view(request):
    all_images = UploadedImage.objects.all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            new_image = UploadedImage(image=uploaded_image)
            new_image.save()
    else:
        form = ImageUploadForm()

    context = {'form': form, 'images': all_images if all_images.exists() else []}

    return render(request, 'dashboard_upload_edit.html', context)

@login_required(login_url='/')
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    # Check if the request method is POST (only allow POST requests for deletion)
    if request.method == 'POST':
        # Delete the image from storage
        image.image.delete()

        # Delete the image record from the database
        image.delete()

    all_images = UploadedImage.objects.all()

    form = ImageUploadForm()

    context = {'form': form, 'images': all_images if all_images.exists() else []}

    # Redirect back to the dashboard with images
    return render(request, 'dashboard_upload.html', context)

# shows the preprocess page
@login_required(login_url='/')
def preprocess_view(request):
    all_images = UploadedImage.objects.all()
    context = {'images': all_images}
    
    return render(request, 'preprocess.html', context)

# processes the image based off of settings selection
def process_image(request):
    operation = request.POST.get('operation')
    image_url = request.POST.get('image_url')

    # Decode Base64 image data
    image_bytes = base64.b64decode(image_url.split(',')[1])

    # Convert image data to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if operation == 'grayscale':
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == 'labcolor':
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif operation == 'rgb':
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif operation == 'redchannel' or operation == 'bluechannel' or operation == 'greenchannel':
        blue_channel, green_channel, red_channel = cv2.split(image)
        if operation == 'redchannel':
            processed_image = red_channel
        elif operation == 'greenchannel':
            processed_image = green_channel
        elif operation == 'bluechannel':
            processed_image = blue_channel
    elif operation == 'HE':
        processed_image = cv2.equalizeHist(image)
    elif operation == 'CS':
        min_val, max_val, _, _ = cv2.minMaxLoc(image)
        processed_image = np.uint8((image - min_val) / (max_val - min_val) * 255)
    elif operation == 'GC':
        gamma = 1.5
        processed_image = np.uint8(((image / 255.0) ** gamma) * 255)
    elif operation == 'AHE':
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        processed_image = clahe.apply(image)
    elif operation == 'SC':
        processed_image = (sigmoid_correction(image) * 255).astype(np.uint8)
    elif operation == 'LHE':
        processed_image = exposure.equalize_adapthist(image, clip_limit=0.03)
    elif operation == 'PLS':
        min_val, max_val = 50, 200
        processed_image = piecewise_linear(image, min_val, max_val)
    else:
        return JsonResponse({'error': 'Unsupported operation'})

    _, buffer = cv2.imencode('.jpg', processed_image)
    processed_image_base64 = base64.b64encode(buffer).decode()
    return JsonResponse({'processed_image': 'data:image/jpeg;base64,' + processed_image_base64})

    
# Apply sigmoid correction
def sigmoid_correction(image, alpha=10, beta=0.5):
    return 1 / (1 + np.exp(-alpha * (image / 255.0 - beta)))

# Apply piecewise linear contrast stretching
def piecewise_linear(image, min_val, max_val):
    return np.clip((image - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)