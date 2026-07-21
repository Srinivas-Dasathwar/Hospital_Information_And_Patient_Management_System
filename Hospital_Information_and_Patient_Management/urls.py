"""
URL configuration for Hospital_Information_and_Patient_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from doctor import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('add_prescription/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
    path('payment/<int:appointment_id>/', views.make_payment, name='make_payment'),
    path('download_prescription/<int:prescription_id>/', views.download_prescription, name='download_prescription'),
    path(
    'download_file/<int:prescription_id>/',
    views.download_file,
    name='download_file'
    ),
    path(
        'hospital/<int:hospital_id>/',
        views.hospital_details,
        name='hospital_details'
    ),
    path(
        'hospitals/',
        views.hospital_search,
        name='hospital_search'
    ),
    path(
        'send_otp/',
        views.send_otp,
        name='send_otp'
    )
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )