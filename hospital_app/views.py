from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Database connection helper
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="lk_hospital_db"
    )

# Home/Dashboard
def home(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM billing")
    total_billing = cursor.fetchone()[0]

    cursor.execute("SELECT patient_name, doctor_name, appointment_date, symptoms FROM appointments ORDER BY appointment_date DESC LIMIT 5")
    appts = cursor.fetchall()
    recent_appointments = [
        {
            "patient_name": row[0],
            "doctor_name": row[1],
            "appointment_date": row[2],
            "symptoms": row[3],
        }
        for row in appts
    ]
    cursor.close()
    db.close()
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'home.html', {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'total_billing': total_billing,
        'recent_appointments': recent_appointments,
        'username': username,
    })

# All appointments
def appointments(request):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, 'appointments.html', {'appointments': appointments})

def add_appointment(request):
    if request.method == "POST":
        name = request.POST['patient_name']
        doctor = request.POST['doctor_name']
        date_str = request.POST['appointment_date']
        symptoms = request.POST['symptoms']
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO appointments (patient_name, doctor_name, appointment_date, symptoms) VALUES (%s, %s, %s, %s)",
                (name, doctor, date, symptoms)
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect('appointments')
        except ValueError:
            return HttpResponse("❌ Invalid date format. Please use YYYY-MM-DD.")
    return render(request, 'add_appointment.html')

def update_appointment(request, appt_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appt_id,))
    appointment = cursor.fetchone()
    if not appointment:
        cursor.close()
        db.close()
        return HttpResponse("❌ Appointment not found.")

    if request.method == "POST":
        name = request.POST.get('patient_name') or appointment[1]
        doctor = request.POST.get('doctor_name') or appointment[2]
        date_input = request.POST.get('appointment_date')
        symptoms = request.POST.get('symptoms') or appointment[4]
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date() if date_input else appointment[3]
            cursor.execute(
                "UPDATE appointments SET patient_name=%s, doctor_name=%s, appointment_date=%s, symptoms=%s WHERE id=%s",
                (name, doctor, date, symptoms, appt_id)
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect('appointments')
        except ValueError:
            cursor.close()
            db.close()
            return HttpResponse("❌ Invalid date format.")
    cursor.close()
    db.close()
    return render(request, 'update_appointment.html', {'appointment': appointment})

def delete_appointment(request, appt_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appt_id,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appt_id,))
        db.commit()
        cursor.close()
        db.close()
        return redirect('appointments')
    else:
        cursor.close()
        db.close()
        return HttpResponse("❌ Appointment not found.")

# Patients
def patients(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    patients_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, 'patients.html', {'patients': patients_data})

def add_patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        contact = request.POST.get('contact')
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO patients (name, gender, age, contact) VALUES (%s, %s, %s, %s)",
            (name, gender, age, contact)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('patients')
    return render(request, 'add_patient.html')

def update_patient(request, patient_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    if not patient:
        cursor.close()
        db.close()
        return HttpResponse("❌ Patient not found.")

    if request.method == "POST":
        name = request.POST.get('name') or patient[1]
        gender = request.POST.get('gender') or patient[2]
        age = request.POST.get('age') or patient[3]
        contact = request.POST.get('contact') or patient[4]
        cursor.execute(
            "UPDATE patients SET name=%s, gender=%s, age=%s, contact=%s WHERE id=%s",
            (name, gender, age, contact, patient_id)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('patients')
    cursor.close()
    db.close()
    return render(request, 'update_patient.html', {'patient': patient})

def delete_patient(request, patient_id):
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
            db.commit()
            cursor.close()
            db.close()
            return redirect('patients')
        else:
            cursor.close()
            db.close()
            return HttpResponse("❌ Patient not found.")
    else:
        return HttpResponse("❌ Invalid request method.")

# Doctors
def doctors(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors_list = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, 'doctors.html', {'doctors': doctors_list})

def add_doctor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        specialty = request.POST.get('specialty')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO doctors (name, specialty, contact, gender) VALUES (%s, %s, %s, %s)",
            (name, specialty, contact, gender)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('doctors')
    return render(request, 'add_doctor.html')

def update_doctor(request, doctor_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()
    if not doctor:
        cursor.close()
        db.close()
        return HttpResponse("❌ Doctor not found.")

    if request.method == "POST":
        name = request.POST.get('name') or doctor[1]
        specialty = request.POST.get('specialty') or doctor[2]
        gender = request.POST.get('gender') or doctor[3]
        contact = request.POST.get('contact') or doctor[4]
        email = request.POST.get('email') or doctor[5]
        cursor.execute(
            "UPDATE doctors SET name=%s, specialty=%s, gender=%s, contact=%s, email=%s WHERE id=%s",
            (name, specialty, gender, contact, email, doctor_id)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('doctors')
    cursor.close()
    db.close()
    return render(request, 'update_doctor.html', {'doctor': doctor})

def delete_doctor(request, doctor_id):
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
            db.commit()
            cursor.close()
            db.close()
            return redirect('doctors')
        else:
            cursor.close()
            db.close()
            return HttpResponse("❌ Doctor not found.")
    else:
        return HttpResponse("❌ Invalid request method.")

# Billing
def billing(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT b.id, p.name, b.amount, b.description, b.date, b.status
        FROM billing b
        LEFT JOIN patients p ON b.patient_id = p.id
    """)
    bills = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, 'billing.html', {'bills': bills})

def add_bill(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    if request.method == "POST":
        patient_id = request.POST.get('patient_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        status = request.POST.get('status', 'unpaid')
        cursor.execute(
            "INSERT INTO billing (patient_id, amount, description, date, status) VALUES (%s, %s, %s, %s, %s)",
            (patient_id, amount, description, date, status)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('billing')
    cursor.close()
    db.close()
    return render(request, 'add_bill.html', {'patients': patients})

def update_bill(request, bill_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM billing WHERE id = %s", (bill_id,))
    bill = cursor.fetchone()
    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    if not bill:
        cursor.close()
        db.close()
        return HttpResponse("❌ Bill not found.")
    if request.method == "POST":
        patient_id = request.POST.get('patient_id') or bill[1]
        amount = request.POST.get('amount') or bill[2]
        description = request.POST.get('description') or bill[3]
        date = request.POST.get('date') or bill[4]
        status = request.POST.get('status') or bill[5]
        cursor.execute(
            """UPDATE billing SET patient_id=%s, amount=%s, description=%s, date=%s, status=%s WHERE id=%s""",
            (patient_id, amount, description, date, status, bill_id)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('billing')
    cursor.close()
    db.close()
    return render(request, 'update_bill.html', {'bill': bill, 'patients': patients})

def delete_bill(request, bill_id):
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM billing WHERE id = %s", (bill_id,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM billing WHERE id = %s", (bill_id,))
            db.commit()
            cursor.close()
            db.close()
            return redirect('billing')
        else:
            cursor.close()
            db.close()
            return HttpResponse("❌ Bill not found.")
    else:
        return HttpResponse("❌ Invalid request method.")

def settings_view(request):
    return render(request, 'settings.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    success = False
    if request.method == 'POST':
        # You can handle saving or emailing the contact message here if needed
        success = True
    return render(request, 'contact.html', {'success': success})

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
            # Auto-login after registration
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    return render(request, 'registration.html', {'error': error})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password."
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def view_appointments(request):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT a.id, p.name, d.name, a.appointment_date, a.symptoms
        FROM appointments a
        LEFT JOIN patients p ON a.patient_id = p.id
        LEFT JOIN doctors d ON a.doctor_id = d.id
    """)
    appointments = cursor.fetchall()
    cursor.close()
    db.close()
    return render(request, 'view_appointments.html', {'appointments': appointments})