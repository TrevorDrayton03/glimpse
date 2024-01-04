from django.db import models
from django.contrib.auth.models import User 

class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='user_images/') # this requires pilows to be installed
