# any time this file is changed you need to run the following commands
# python manage.py makemigrations
# python manage.py migrate

import os
from django.db import models

def overwrite_filename(instance, filename):
    return os.path.join('preprocessed_images/', filename)

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)

# establishes a one to one relationship with the original image and its preprocessed image
# ensures that if it is deleted then its uploadedimage is deleted as well (models.cascade)
class PreprocessedImage(models.Model):
    original_image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='preprocessed_image')
    image = models.ImageField(upload_to=overwrite_filename)

    # overwrites the save method to delete the old image
    # ex: 601.jpg gets created, the process_image view saves it as 601_X9Y28.jpg, then 601.jpg gets deleted
    def save(self, *args, **kwargs):
        if self.pk:
            existing_obj = PreprocessedImage.objects.get(pk=self.pk)
            if existing_obj.image and self.image != existing_obj.image:
                existing_obj.image.delete(save=False)
        super().save(*args, **kwargs)
