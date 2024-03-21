from django.contrib import admin
from django.urls import path
from capstone_UI_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main_view, name='main'),
    path('adminLoginOnly', admin.site.urls),
    path('login/', views.custom_login_view.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register_view, name='register'),
    path('billing/', views.billing_view, name='billing'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('dashboard/upload/', views.dashboard_upload_view, name='dashboard_upload'),
    path('dashboard/upload/camera/', views.dashboard_upload_camera_view, name='dashboard_upload_camera'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete_image/<int:image_id>/review', views.delete_image_review, name='delete_image_review'),
    path('delete_all_images/', views.delete_all_images, name='delete_all_images'),
    path('preprocess/',views.preprocess_view, name="preprocess"),
    path('process_image/', views.process_image, name='process_image'),
    path('review/',views.review_view, name="review"),
    path('thankyou/',views.thankyou_view, name="thankyou"),
    path('run_inference/', views.run_inference, name='run_inference'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('revert_preprocessed_image/', views.revert_preprocessed_image, name='revert_preprocessed_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

