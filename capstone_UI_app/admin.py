from django.contrib import admin
from .models import UploadedImage, PreprocessedImage

admin.site.register(UploadedImage)
admin.site.register(PreprocessedImage)