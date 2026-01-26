"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from patient import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('home/', views.home, name='home'),

    # Patient detail
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),

    # Delete patient
    path('patient/<int:pk>/delete/', views.delete_patient, name='delete_patient'),

    # Add patient
    path('add_patient/', views.add_patient, name='add_patient'),

    # Appointments
    path('appointments/', views.appointments, name='appointments'),
]

