from django.contrib import admin
from django.urls import path
from capstone_UI_app import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('login/', views.custom_login_view.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('contact/', views.contact_view, name='contact'),
    path('billing/', views.billing_view, name='billing'),
    path('thankyou/', views.thankyou_view, name='thankyou'),
]
