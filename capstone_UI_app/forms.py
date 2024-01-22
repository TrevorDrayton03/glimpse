from django import forms
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

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)

class ImageUploadForm(forms.Form):
    image = forms.ImageField(validators=[
        # Validate file size (e.g., 2 MB)
        #forms.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        #forms.FileSizeValidator(max_size=2 * 1024 * 1024),  # 2 MB

        # Validate image dimensions (e.g., 800x600 pixels)
       # forms.ImageField(width_field=800, height_field=600),
        forms.ImageField()
    ])