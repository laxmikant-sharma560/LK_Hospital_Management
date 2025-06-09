from django.urls import path
from .views import (
    home, about, contact, settings_view,
    AppointmentListView, AppointmentCreateView, AppointmentUpdateView, AppointmentDeleteView,
    PatientListView, PatientCreateView, PatientUpdateView, PatientDeleteView,
    DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView,
    BillingListView, BillingCreateView, BillingUpdateView, BillingDeleteView,
    DepartmentListView,
    register, login_view, logout_view,
)

urlpatterns = [
    # Dashboard/Home
    path('', home, name='home'),

    # Appointments (CBV)
    path('appointments/', AppointmentListView.as_view(), name='appointments'),
    path('appointments/add/', AppointmentCreateView.as_view(), name='add_appointment'),
    path('appointments/<int:pk>/edit/', AppointmentUpdateView.as_view(), name='update_appointment'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='delete_appointment'),

    # Patients (CBV)
    path('patients/', PatientListView.as_view(), name='patients'),
    path('patients/add/', PatientCreateView.as_view(), name='add_patient'),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name='update_patient'),
    path('patients/<int:pk>/delete/', PatientDeleteView.as_view(), name='delete_patient'),

    # Doctors (CBV)
    path('doctors/', DoctorListView.as_view(), name='doctors'),
    path('doctors/add/', DoctorCreateView.as_view(), name='add_doctor'),
    path('doctors/<int:pk>/edit/', DoctorUpdateView.as_view(), name='update_doctor'),
    path('doctors/<int:pk>/delete/', DoctorDeleteView.as_view(), name='delete_doctor'),

    # Billing (CBV)
    path('billing/', BillingListView.as_view(), name='billing'),
    path('billing/add/', BillingCreateView.as_view(), name='add_bill'),
    path('billing/<int:pk>/edit/', BillingUpdateView.as_view(), name='update_bill'),
    path('billing/<int:pk>/delete/', BillingDeleteView.as_view(), name='delete_bill'),

    # Departments (CBV, list only)
    path('departments/', DepartmentListView.as_view(), name='departments'),

    # Info & settings (function views)
    path('settings/', settings_view, name='settings'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    # Auth
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]