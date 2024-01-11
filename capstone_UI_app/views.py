from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ContactForm, BillingForm

def welcome_view(request):
    return render(request, 'welcome.html')

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