from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ContactForm, BillingForm, RegisterForm, ImageUploadForm
from .models import UploadedImage

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
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def thankyou_view(request):
    return render(request, 'thankyou.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

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
