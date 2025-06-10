from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import Patient, Doctor, Appointment, Billing, Department
from .forms import PatientForm, DoctorForm, AppointmentForm, BillingForm

# --- DASHBOARD HOME ---
@login_required
def home(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_billing': Billing.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor').order_by('-appointment_date')[:5],
    }
    return render(request, 'home.html', context)

# --- ADVANCED APPOINTMENTS LIST WITH SEARCH/FILTER/SORT/PAGINATION & AJAX ---
class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10

    def get_queryset(self):
        qs = Appointment.objects.select_related('patient', 'doctor', 'department')
        q = self.request.GET.get('q', '').strip()
        doctor_id = self.request.GET.get('doctor')
        dept_id = self.request.GET.get('department')
        date = self.request.GET.get('date')
        sort = self.request.GET.get('sort', '-appointment_date')

        if q:
            qs = qs.filter(
                Q(patient__name__icontains=q) |
                Q(doctor__name__icontains=q) |
                Q(symptoms__icontains=q)
            )
        if doctor_id:
            qs = qs.filter(doctor_id=doctor_id)
        if dept_id:
            qs = qs.filter(doctor__department_id=dept_id)
        if date:
            qs = qs.filter(appointment_date=date)
        if sort:
            qs = qs.order_by(sort)
        return qs

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            appointments = [
                {
                    'id': appt.id,
                    'patient': appt.patient.name,
                    'doctor': appt.doctor.name,
                    'date': appt.appointment_date,
                    'symptoms': appt.symptoms
                }
                for appt in context['appointments']
            ]
            return JsonResponse({'appointments': appointments})
        return super().render_to_response(context, **response_kwargs)

# --- APPOINTMENT CRUD (CBVs) ---
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'add_app.html'
    success_url = reverse_lazy('appointments')
    def form_valid(self, form):
        messages.success(self.request, "Appointment created successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'update_appointment.html'
    success_url = reverse_lazy('appointments')
    def form_valid(self, form):
        messages.success(self.request, "Appointment updated successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('appointments')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Appointment deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- PATIENT CRUD (CBVs) WITH FILTER/SEARCH ---
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients.html'
    context_object_name = 'patients'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = Patient.objects.all()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
        return qs.order_by('name')

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'add_patient.html'
    success_url = reverse_lazy('patients')
    def form_valid(self, form):
        messages.success(self.request, "Patient added successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'update_patient.html'
    success_url = reverse_lazy('patients')
    def form_valid(self, form):
        messages.success(self.request, "Patient updated successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('patients')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Patient deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- DOCTOR CRUD (CBVs) WITH ADVANCED FILTER ---
class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        dept = self.request.GET.get('department')
        qs = Doctor.objects.all()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
        if dept:
            qs = qs.filter(department_id=dept)
        return qs.order_by('name')

class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'add_doctor.html'
    success_url = reverse_lazy('doctors')
    def form_valid(self, form):
        messages.success(self.request, "Doctor added successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'update_doctor.html'
    success_url = reverse_lazy('doctors')
    def form_valid(self, form):
        messages.success(self.request, "Doctor updated successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('doctors')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Doctor deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- BILLING CRUD (CBVs) ---
class BillingListView(LoginRequiredMixin, ListView):
    model = Billing
    template_name = 'billing.html'
    context_object_name = 'bills'
    paginate_by = 10
    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = Billing.objects.select_related('patient', 'appointment')
        if q:
            qs = qs.filter(Q(patient__name__icontains=q) | Q(description__icontains=q))
        return qs.order_by('-date')

class BillingCreateView(LoginRequiredMixin, CreateView):
    model = Billing
    form_class = BillingForm
    template_name = 'add_bill.html'
    success_url = reverse_lazy('billing')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        return context
    def form_valid(self, form):
        messages.success(self.request, "Bill added successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class BillingUpdateView(LoginRequiredMixin, UpdateView):
    model = Billing
    form_class = BillingForm
    template_name = 'update_bill.html'
    success_url = reverse_lazy('billing')
    def form_valid(self, form):
        messages.success(self.request, "Bill updated successfully.")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Error: " + str(form.errors))
        return super().form_invalid(form)

class BillingDeleteView(LoginRequiredMixin, DeleteView):
    model = Billing
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('billing')
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Bill deleted successfully.")
        return super().delete(request, *args, **kwargs)

# --- DEPARTMENT LIST (FILTER) ---
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'departments.html'
    context_object_name = 'departments'
    paginate_by = 10

# --- SETTINGS, ABOUT, CONTACT ---
@login_required
def settings_view(request):
    return render(request, 'settings.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    success = False
    if request.method == 'POST':
        # Save or email contact message here if needed
        success = True
        messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
    return render(request, 'contact.html', {'success': success})

# --- AUTH USER REGISTRATION & LOGIN ---
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

def register(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email already registered."
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Registration successful! Welcome.")
                return redirect('home')
    if error:
        messages.error(request, error)
    return render(request, 'registration.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful. Welcome.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# --- BILLING FORM (Function-based View, Optional) ---
@login_required
def add_bill(request):
    """
    Show and process the add bill form. Uses BillingForm for validation.
    """
    if request.method == "POST":
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Bill added successfully.")
            return redirect('billing')
        else:
            messages.error(request, "Error: " + str(form.errors))
    else:
        form = BillingForm()
    patients = Patient.objects.all()
    return render(request, 'add_bill.html', {'form': form, 'patients': patients})


