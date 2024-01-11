from django.contrib import admin
from django.urls import path
from capstone_UI_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('login/', views.custom_login_view.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register_view, name='register'),
    path('billing/', views.billing_view, name='billing'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
    path('dashboard/upload/', views.upload_image, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
