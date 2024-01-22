from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)