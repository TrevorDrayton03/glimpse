import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from django.conf import settings
from .forms import ContactForm, BillingForm, RegisterForm, ImageUploadForm
from .models import UploadedImage, PreprocessedImage
from .apps import CapstoneUiAppConfig, initialize_and_predict
from .pdf_report import generate_pdf_report
from django.core.files.base import ContentFile
from django.core.serializers import serialize

# python libraries for preprocessing
import cv2
import numpy as np
import base64
from skimage import exposure


def main_view(request):
    if request.GET.get('ajax') == '1':
        # If it's an AJAX request, return the AJAX template (so that the base template does not get loaded inside itself)
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
    # all_images = UploadedImage.objects.all()
    all_images = UploadedImage.objects.prefetch_related('preprocessed_image').all()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            
            new_image = UploadedImage(image=uploaded_image)
            new_image.save()

            PreprocessedImage.objects.create(original_image=new_image, image=uploaded_image)

    else:
        form = ImageUploadForm()

    context = {'form': form, 'images': all_images if all_images.exists() else []}

    return render(request, 'dashboard_upload.html', context)

@login_required(login_url="/")
def dashboard_upload_camera_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            
            new_image = UploadedImage(image=uploaded_image)
            new_image.save()
            
            PreprocessedImage.objects.create(original_image=new_image, image=uploaded_image)
    
        all_images = UploadedImage.objects.prefetch_related('preprocessed_image').all()
        context = {'images': all_images if all_images.exists() else []}
        # After saving the new image
        return JsonResponse({'success': True, 'imageUrl': new_image.image.url})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid form submission'})


@login_required(login_url='/')
def delete_image(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    # Check if the request method is POST (only allow POST requests for deletion)
    if request.method == 'POST':
        # Attempt to retrieve the related preprocessed image
        preprocessed_image = PreprocessedImage.objects.filter(original_image=image).first()
        
        # If a preprocessed image exists, delete it
        if preprocessed_image:
            preprocessed_image.image.delete()  # Delete the file from storage
            preprocessed_image.delete()  # Delete the preprocessed image record from the database

        # Delete the original image from storage
        image.image.delete()

        # Delete the original image record from the database
        image.delete()

    all_images = UploadedImage.objects.all()
    form = ImageUploadForm()
    context = {'form': form, 'images': all_images if all_images.exists() else []}

    # Redirect back to the dashboard with images
    return render(request, 'dashboard_upload.html', context)

@login_required(login_url='/')
def delete_image_review(request, image_id):
    image = get_object_or_404(UploadedImage, id=image_id)
    # Check if the request method is POST (only allow POST requests for deletion)
    if request.method == 'POST':
        # Attempt to retrieve the related preprocessed image
        preprocessed_image = PreprocessedImage.objects.filter(original_image=image).first()
        
        # If a preprocessed image exists, delete it
        if preprocessed_image:
            preprocessed_image.image.delete()  # Delete the file from storage
            preprocessed_image.delete()  # Delete the preprocessed image record from the database

        # Delete the original image from storage
        image.image.delete()

        # Delete the original image record from the database
        image.delete()

    all_images = UploadedImage.objects.all()
    # print(all_images)
    form = ImageUploadForm()
    context = {'form': form, 'images': all_images if all_images.exists() else []}

    # Redirect back to the dashboard with images
    return render(request, 'review.html', context)

# shows the preprocess page
@login_required(login_url='/')
def preprocess_view(request):
    all_images = UploadedImage.objects.prefetch_related('preprocessed_image').all()
    all_images_json = serialize('json', all_images)
    preprocessed_images = PreprocessedImage.objects.all()
    preprocessed_filenames = get_preprocessed_image_filenames();
    context = {'images': all_images, 'images_json': all_images_json, 'preprocessed_images': preprocessed_images, 'preprocessed_filenames': preprocessed_filenames}
    
    return render(request, 'preprocess.html', context)

def get_preprocessed_image_filenames():
    # Define the directory path
    directory = 'media/preprocessed_images/'
    
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Filter out directories and return only filenames
    filenames = [os.path.join(directory, filename) for filename in files if os.path.isfile(os.path.join(directory, filename))]
    
    return filenames

# processes the image based off of settings selection
def process_image(request):
    scale = 2.0
    image_data = request.POST.get('image_data')
    image_id = request.POST.get('image_id')
    image_name = request.POST.get('image_name')
    image_bytes = base64.b64decode(image_data.split(',')[1] if len(image_data.split(',')) > 1 else "")
    nparr = np.frombuffer(image_bytes, np.uint8)
    original_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    operation = request.POST.get('operation')
    sliderType = request.POST.get('sliderType')
    sliderValue = int(request.POST.get('sliderValue', 50))

    adjustment = (sliderValue - 50) * scale
    # Decode Base64 image data
    image_bytes = base64.b64decode(image_data.split(',')[1])

    # Convert image data to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the image using OpenCV
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    newImage = original_image.copy()

    try:
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
            if len(image.shape) > 2:
                processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                processed_image = image.copy()

            processed_image = cv2.convertScaleAbs(processed_image)
            processed_image = cv2.equalizeHist(processed_image)
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
        elif sliderType == 'brightness':
            # print(adjustment)
            if adjustment != 0:
                hsv = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                v = cv2.add(v, adjustment)
                v = np.clip(v, 0, 255)
                final_hsv = cv2.merge((h, s, v))
                processed_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        elif sliderType == 'saturation':
            if adjustment != 0:
                hsv = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                s = cv2.add(s, adjustment)
                s = np.clip(s, 0, 255)
                final_hsv = cv2.merge((h, s, v))
                processed_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        elif sliderType =='sharpness':
            if adjustment != 0:
                sharpness_filter = np.array([[-1, -1, -1],
                                             [-1, 9 + adjustment / 10, -1],
                                             [-1, -1, -1]])
                processed_image = cv2.filter2D(newImage, -1, sharpness_filter)
        else:
            return JsonResponse({'error': 'Unsupported operation'})
        
        _, buffer = cv2.imencode('.jpg', processed_image)
        processed_image_base64 = base64.b64encode(buffer).decode()

        #### Save the processed image ####
        try:
            image = UploadedImage.objects.get(id=image_id)
            preprocessed_image = PreprocessedImage.objects.filter(original_image=image).first()
            preprocessed_image.image.save(image_name, ContentFile(buffer), save=True)
        except UploadedImage.DoesNotExist:
            print("Image not found")
        ##################################
        preprocessed_filenames = get_preprocessed_image_filenames()
        return JsonResponse({'processed_image': 'data:image/jpeg;base64,' + processed_image_base64, 'preprocessed_filenames': preprocessed_filenames})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
def revert_preprocessed_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        try:
            image = UploadedImage.objects.get(id=image_id)
        except UploadedImage.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Image not found'})

        preprocessed_image = PreprocessedImage.objects.filter(original_image=image).first()
        if preprocessed_image:
            # Save the original image over the preprocessed image
            try:
                # Use the filename of the preprocessed image
                filename = os.path.basename(preprocessed_image.image.name)
                preprocessed_image.image.save(filename, image.image.file, save=True)
                preprocessed_filenames = get_preprocessed_image_filenames()
                return JsonResponse({'success': True, 'message': 'Original image saved over preprocessed image', 'preprocessed_filenames': preprocessed_filenames})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error saving image: {str(e)}'})
        else:
            return JsonResponse({'success': False, 'message': 'Preprocessed image not found for the specified image'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    
# Apply sigmoid correction
def sigmoid_correction(image, alpha=10, beta=0.5):
    return 1 / (1 + np.exp(-alpha * (image / 255.0 - beta)))

# Apply piecewise linear contrast stretching
def piecewise_linear(image, min_val, max_val):
    return np.clip((image - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)

@login_required(login_url='/')
def review_view(request):
    # all_images = UploadedImage.objects.all()
    all_images = UploadedImage.objects.prefetch_related('preprocessed_image').all()
    context = {'images': all_images}
    return render(request, 'review.html', context)

@login_required(login_url='/')
def run_inference(request):
    if request.method == 'POST':
        model = CapstoneUiAppConfig.model
        if model is not None:
            images = UploadedImage.objects.all()
            inference_results = []
            if images.exists():  
                for image in images:
                    prediction, probabilities = initialize_and_predict(image.image.path)
                    print(f"Predicted class: {prediction}, Probabilities: {probabilities}")
                    image_path = image.image.path
                    results = model([image_path])  
                    for result in results:
                        # raw_confidences = result.probs[:, -1].cpu().numpy()
                        # print(raw_confidences, " raw_confidences")
                        # confidences = result.xyxy[:, 4]
                        # print(confidences, " confidences")
                        annotated_image_path = image_path.replace('.jpg', '_annotated.jpg')
                        result.save(annotated_image_path)  
                        result_data = {
                            "original_path": image_path,
                            "processed_path": image_path,
                            "boxes": result.boxes,
                            "annotated_image_path": annotated_image_path,
                        }
                        # result.show()
                        inference_results.append(result_data)
                        print(result.boxes.conf, " result.boxes.conf")
                        
                pdf_path = os.path.join(settings.BASE_DIR, 'GLIMPSE.pdf')
                generate_pdf_report(inference_results, pdf_path)
                return render(request, 'thankyou.html')
            else:
                return HttpResponse("No images found for inference.")
        else:
            return HttpResponse("Model not loaded.")
    else:
        return HttpResponse("This endpoint expects a POST request.")

def download_pdf(request):
    pdf_path = os.path.join(settings.BASE_DIR, 'GLIMPSE.pdf')
    response = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="GLIMPSE.pdf"'
    return response