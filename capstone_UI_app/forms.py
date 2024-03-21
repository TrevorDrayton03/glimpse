from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Import the User model
# from django.core.exceptions import ValidationError
# from PIL import Image

class ContactForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=100)
    email = forms.EmailField(label='Email')
    physical_address = forms.CharField(label='Physical Address', max_length=255)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    city = forms.CharField(label='City', max_length=50)
    province_or_territory = forms.CharField(label='Province/Territory', max_length=50)
    postal_code = forms.CharField(label='Postal Code', max_length=10)
    healthcare_number = forms.CharField(label='Healthcare Number', max_length=50)

class BillingForm(forms.Form):
    billing_address = forms.CharField(label='Billing Address', max_length=255)
    billing_city = forms.CharField(label='Billing City', max_length=50)
    billing_province_or_territory = forms.CharField(label='Billing Province/Territory', max_length=50)
    billing_postal_code = forms.CharField(label='Billing Postal Code', max_length=10)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class ImageUploadForm(forms.Form):
    # image = forms.ImageField()

    # update to multiple image upload
    image = MultipleFileField()

class ImagePreProcessForm(forms.Form):
    image = forms.ImageField()