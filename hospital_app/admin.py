from django.contrib import admin
from .models import Patient, Doctor, Appointment, Billing

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'gender', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'specialty', 'phone', 'email', 'created_at']
    search_fields = ['name', 'specialty']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment_date', 'created_at']
    list_filter = ['appointment_date']
    search_fields = ['patient__name', 'doctor__name']

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'amount', 'date', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['patient__name', 'description']