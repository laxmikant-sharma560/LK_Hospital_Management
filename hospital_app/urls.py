from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Appointments management URLs
    path('appointments/', views.appointments, name='appointments'),  # List all appointments
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/update/<int:appt_id>/', views.update_appointment, name='update_appointment'),
    path('appointments/delete/<int:appt_id>/', views.delete_appointment, name='delete_appointment'),

    # Patients management URLs
    path('patients/', views.patients, name='patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/update/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    # Doctors management URLs
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/update/<int:doctor_id>/', views.update_doctor, name='update_doctor'),
    path('doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),

    # Billing management URLs
    path('billing/', views.billing, name='billing'),
    path('billing/add/', views.add_bill, name='add_bill'),
    path('billing/update/<int:bill_id>/', views.update_bill, name='update_bill'),
    path('billing/delete/<int:bill_id>/', views.delete_bill, name='delete_bill'),

    # Settings
    path('settings/', views.settings_view, name='settings'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]