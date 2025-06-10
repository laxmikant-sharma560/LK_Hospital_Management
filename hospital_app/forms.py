# hospital_app/forms.py

from django import forms
from .models import Patient, Doctor, Appointment, Billing
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'