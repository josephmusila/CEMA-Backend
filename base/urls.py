# health_info/urls.py
from django.urls import path
from .views import (
    HealthProgramCreateListView, ClientCreateListView, EnrollmentCreateView,
    ClientProfileView, DoctorRegisterView
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', DoctorRegisterView.as_view(), name='doctor-register'),
    path('login/', obtain_auth_token, name='login'),
    path('programs/', HealthProgramCreateListView.as_view(), name='program-list-create'),
    path('clients/', ClientCreateListView.as_view(), name='client-list-create'),
    path('enrollments/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('clients/<int:pk>/', ClientProfileView.as_view(), name='client-profile'),
]