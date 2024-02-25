# any time this file is changed you need to run the following commands
# python manage.py makemigrations
# python manage.py migrate

from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)

# establishes a one to one relationship with the original image and its preprocessed image
# ensures that if it is deleted then its uploadedimage is deleted as well (models.cascade)
class PreprocessedImage(models.Model):
    original_image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='preprocessed_image')
    image = models.ImageField(upload_to='preprocessed_images/')