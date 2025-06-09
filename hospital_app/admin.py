from django.contrib import admin
from .models import (
    Patient, Doctor, Appointment, Department, Nurse, Room, MedicalRecord,
    Billing, Prescription, PrescriptionItem, Staff
)

# --- Inlines ---
class AppointmentInline(admin.TabularInline):
    model = Appointment
    fields = ['doctor', 'department', 'appointment_date', 'appointment_time', 'status']
    extra = 0
    show_change_link = True

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    extra = 0
    show_change_link = True

class BillingInline(admin.TabularInline):
    model = Billing
    fields = ['amount', 'date', 'status']
    extra = 0
    show_change_link = True

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0
    show_change_link = True

# --- Patient ---
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'gender', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['gender', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AppointmentInline, MedicalRecordInline, BillingInline, PrescriptionInline]
    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'age', 'gender', 'photo')
        }),
        ("Contact", {
            'fields': ('address', 'phone', 'email', 'emergency_contact')
        }),
        ("System Info", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# --- Doctor ---
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'specialty', 'phone', 'email', 'is_active', 'created_at']
    search_fields = ['name', 'specialty', 'department__name']
    list_filter = ['department', 'is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AppointmentInline, MedicalRecordInline, PrescriptionInline]
    fieldsets = (
        ("Doctor Info", {
            'fields': ('name', 'user', 'department', 'specialty', 'biography', 'photo', 'is_active')
        }),
        ("Contact", {
            'fields': ('phone', 'email')
        }),
        ("System Info", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# --- Appointment ---
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['appointment_date', 'doctor', 'department', 'status']
    search_fields = ['patient__name', 'doctor__name', 'symptoms']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status')
        }),
        ("Details", {
            'fields': ('symptoms', 'notes')
        }),
        ("System Info", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# --- Department ---
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    ordering = ['name']

# --- Nurse ---
@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'gender', 'phone', 'email', 'is_active', 'created_at']
    search_fields = ['name', 'department__name', 'phone']
    list_filter = ['department', 'gender', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

# --- Room ---
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_occupied', 'assigned_patient', 'created_at']
    search_fields = ['room_number']
    list_filter = ['room_type', 'is_occupied']
    readonly_fields = ['created_at']

# --- Medical Record ---
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'diagnosis', 'record_date', 'created_at']
    search_fields = ['patient__name', 'diagnosis']
    list_filter = ['doctor', 'record_date']
    readonly_fields = ['created_at']

# --- Billing ---
@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'appointment', 'amount', 'date', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['patient__name', 'description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('patient', 'appointment', 'amount', 'date', 'status')
        }),
        ("Details", {
            'fields': ('description',),
        }),
        ("System Info", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# --- Prescription & Items ---
class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 0

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'prescribed_date']
    search_fields = ['patient__name', 'doctor__name']
    list_filter = ['doctor', 'prescribed_date']
    inlines = [PrescriptionItemInline]

# --- Staff ---
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'role', 'department', 'phone', 'email', 'is_active', 'created_at']
    search_fields = ['name', 'role', 'department__name', 'phone']
    list_filter = ['role', 'department', 'is_active']
    readonly_fields = ['created_at']
    ordering = ['role', 'name']

# --- Logical Grouping in Admin Site Index ---
admin.site.index_title = "Hospital Admin Dashboard"
admin.site.site_header = "LK Hospital Management Admin"
admin.site.site_title = "LK Hospital Admin Panel"