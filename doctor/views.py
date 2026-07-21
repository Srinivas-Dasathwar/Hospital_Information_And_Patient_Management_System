from django.shortcuts import render,redirect
from .models import (
    Users,
    Doctor,
    Patient,
    Appointment,
    Payment,
    Prescription
)
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from datetime import date

from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator
from .models import Hospital
from django.contrib import messages
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

def home(request):

    appointments = Appointment.objects.all()

    return render(
        request,
        'home.html',
        {
            'appointments': appointments
        }
    )



def signup(request):

    if request.method=="POST":

        role=request.POST['role']

        full_name=request.POST['full_name']
        email=request.POST['email']
        phone=request.POST['phone_no']
        gender=request.POST['gender']
        password=request.POST['password']

        uploaded_photo = request.FILES.get('photo')
        photo_name = None

        if uploaded_photo:
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'photos')
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, uploaded_photo.name)

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_photo.chunks():
                    destination.write(chunk)

            photo_name = uploaded_photo.name


        if Users.objects.filter(email=email).exists():

            return render(
            request,
            'signup.html',
            {'error':'Email already exists'}
            )


        if Users.objects.filter(phone_no=phone).exists():

            return render(
            request,
            'signup.html',
            {'error':'Phone number already exists'}
            )


        uploaded_photo = request.FILES.get('photo')

        file_name = None

        if uploaded_photo:

            upload_dir = os.path.join(
                settings.MEDIA_ROOT,
                'profile_photos'
            )

            os.makedirs(upload_dir, exist_ok=True)

            file_name = uploaded_photo.name

            file_path = os.path.join(
                upload_dir,
                file_name
            )

            with open(file_path, 'wb+') as destination:

                for chunk in uploaded_photo.chunks():

                    destination.write(chunk)
        user = Users.objects.create(
            full_name=full_name,
            email=email,
            phone_no=phone,
            gender=gender,
            role=role,
            password=password,
            date_of_birth='2000-01-01',
            address='Hyderabad'
        )
        hospital = Hospital.objects.get(
            hospital_id=request.POST['hospital_id']
        )


        if role=="Doctor":

            Doctor.objects.create(
                user=user,
                hospital=hospital,
                full_name=full_name,
                specialization=request.POST['specialization'],
                qualification=request.POST['qualification'],
                experience_years=request.POST['experience'],
                consultation_fee=request.POST['fee'],
                availability='Available',
                photo=file_name
            )


        elif role=="Patient":

            Patient.objects.create(
                user=user,
                hospital=hospital,
                full_name=full_name,
                blood_group=request.POST['blood_group'],
                height=request.POST['height'],
                weight=request.POST['weight'],
                medical_history=request.POST['history'],
                photo=file_name
            )
            send_mail(
                subject='Welcome to HIPMS',
                message=f'''
            Dear {full_name},

            Your account has been successfully created.

            Role: {role}

            Thank you for registering with HIPMS.
            ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

        return redirect('login')


    hospitals = Hospital.objects.all()

    return render(
        request,
        'signup.html',
        {
            'hospitals': hospitals
        }
    )


def login(request):

    if request.method == "POST":

        role = request.POST['role']
        email = request.POST['email']
        password = request.POST['password']

        try:

            user = Users.objects.get(
                email=email,
                password=password,
                role=role
            )

            request.session['user_id'] = user.user_id

            return redirect('dashboard')

        except Users.DoesNotExist:

            return render(
                request,
                'login.html',
                {
                    'error': f'Invalid {role} credentials'
                }
            )

    return render(
        request,
        'login.html'
    )

def dashboard(request):

    if not request.session.get('user_id'):
        return redirect('login')

    user = Users.objects.get(
        user_id=request.session['user_id']
    )

    doctor = None
    patient = None
    appointments = None
    prescriptions = None

    doctors = Doctor.objects.all()   # ADD THIS LINE

    if user.role == "Doctor":

        doctor = Doctor.objects.get(
            user=user
        )

        appointments = Appointment.objects.filter(
            doctor=doctor
        ).exclude(
            status='Cancelled'
        )

    elif user.role == "Patient":

        patient = Patient.objects.get(
            user=user
        )

        appointments = Appointment.objects.filter(
            patient=patient
        )

        prescriptions = Prescription.objects.filter(
            patient=patient
        ).order_by('-prescribed_date')

        doctors = Doctor.objects.all()
       
    return render(
        request,
        'dashboard.html',
        {
            'user': user,
            'doctor': doctor,
            'patient': patient,
            'appointments': appointments,
            'prescriptions': prescriptions,
            'doctors': doctors
        }
    )


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Users, Patient, Doctor, Appointment


def book_appointment(request):

    if not request.session.get('user_id'):
        return redirect('login')

    user = Users.objects.get(
        user_id=request.session['user_id']
    )

    patient = Patient.objects.get(
        user=user
    )

    doctors = Doctor.objects.all()

    if request.method == "POST":

        print("POST DATA:", request.POST)

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        reason = request.POST.get('reason')

        if not doctor_id:
            return HttpResponse("Doctor not selected")

        doctor = Doctor.objects.get(
            doctor_id=doctor_id
        )

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status='Pending'
        )

        return redirect('dashboard')

    return render(
        request,
        'book_appointment.html',
        {
            'doctors': doctors,
            'patient': patient
        }
    )

def doctor_appointments(request):

    if not request.session.get('user_id'):
        return redirect('login')

    user = Users.objects.get(
        user_id=request.session['user_id']
    )

    doctor = Doctor.objects.get(
        user=user
    )

    if request.GET.get('accept'):

        appointment = Appointment.objects.get(
            appointment_id=request.GET.get('accept')
        )

        appointment.status = "Accepted"

        appointment.save()

        send_mail(
            subject='Appointment Approved',
            message=f'''
        Dear {appointment.patient.user.full_name},

        Your appointment with Dr. {appointment.doctor.user.full_name}
        on {appointment.appointment_date}
        at {appointment.appointment_time}
        has been approved.

        Thank you,
        HIPMS Team
        ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                appointment.patient.user.email
            ],
            fail_silently=True,
        )

        return redirect(
            'doctor_appointments'
        )

    if request.GET.get('reject'):

        appointment = Appointment.objects.get(
            appointment_id=request.GET.get('reject')
        )

        appointment.status = "Rejected"

        appointment.save()

        send_mail(
            subject='Appointment Rejected',
            message=f'''
        Dear {appointment.patient.user.full_name},

        Unfortunately your appointment request
        has been rejected.

        Please book another slot.

        Thank you,
        HIPMS Team
        ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                appointment.patient.user.email
            ],
            fail_silently=True,
        )

        return redirect(
            'doctor_appointments'
        )

    appointments = Appointment.objects.filter(
        doctor=doctor
    )

    return render(
        request,
        'doctor_appointments.html',
        {
            'appointments': appointments
        }
    )

def logout(request):

    request.session.flush()

    return redirect('login')

from django.shortcuts import render,redirect
from .models import Users,Doctor,Patient


def admin_login(request):

    if request.method=="POST":

        username=request.POST['username']
        password=request.POST['password']

        if username=="admin" and password=="admin123":

            request.session['admin']=True

            return redirect(
            'admin_dashboard'
            )

    return render(
    request,
    'admin_login.html'
    )


def admin_dashboard(request):

    if not request.session.get('admin'):
        return redirect('admin_login')

    # DELETE USER
    if request.GET.get('delete'):

        user = Users.objects.get(
            user_id=request.GET.get('delete')
        )

        user.delete()

        return redirect('admin_dashboard')

    # UPDATE USER
    if request.method == "POST":

        role = request.POST['role']

        user = Users.objects.get(
            user_id=request.POST['id']
        )

        uploaded_photo = request.FILES.get('photo')
        file_name = None

        if uploaded_photo:

            upload_dir = os.path.join(
                settings.MEDIA_ROOT,
                'profile_photos'
            )

            os.makedirs(upload_dir, exist_ok=True)

            file_name = uploaded_photo.name

            file_path = os.path.join(
                upload_dir,
                file_name
            )

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_photo.chunks():
                    destination.write(chunk)

        new_email = request.POST['email']
        new_phone = request.POST['phone_no']

        email_exists = Users.objects.filter(
            email=new_email
        ).exclude(
            user_id=user.user_id
        ).exists()

        if email_exists:
            messages.error(
                request,
                "This email is already used by another user."
            )
            return redirect('admin_dashboard')

        phone_exists = Users.objects.filter(
            phone_no=new_phone
        ).exclude(
            user_id=user.user_id
        ).exists()

        if phone_exists:
            messages.error(
                request,
                "This phone number is already used by another user."
            )
            return redirect('admin_dashboard')

        user.full_name = request.POST['full_name']
        user.email = new_email
        user.phone_no = new_phone

        user.save()

        send_mail(
            subject='Profile Updated',
            message=f'''
Dear {user.full_name},

Your profile details were updated by the administrator.

Email: {user.email}
Phone: {user.phone_no}

Regards,
HIPMS Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        if role == "Doctor":

            doctor = Doctor.objects.get(
                user=user
            )

            doctor.specialization = request.POST['specialization']
            doctor.qualification = request.POST['qualification']
            doctor.experience_years = request.POST['experience']
            doctor.consultation_fee = request.POST['fee']

            if file_name:
                doctor.photo = file_name

            doctor.save()

        elif role == "Patient":

            patient = Patient.objects.get(
                user=user
            )

            patient.blood_group = request.POST['blood_group']
            patient.height = request.POST['height']
            patient.weight = request.POST['weight']
            patient.medical_history = request.POST['history']

            if file_name:
                patient.photo = file_name

            patient.save()

        return redirect('admin_dashboard')

    # CANCEL APPOINTMENT
    if request.GET.get('cancel_appointment'):

        appointment = Appointment.objects.get(
            appointment_id=request.GET.get('cancel_appointment')
        )

        appointment.status = "Cancelled"
        appointment.save()

        return redirect('admin_dashboard')

    # FETCH DATA
    doctor_list = Doctor.objects.all()
    patient_list = Patient.objects.all()
    appointment_list = Appointment.objects.all()
    payment_list = Payment.objects.all()

    doctor_paginator = Paginator(doctor_list, 5)
    patient_paginator = Paginator(patient_list, 5)
    appointment_paginator = Paginator(appointment_list, 5)
    payment_paginator = Paginator(payment_list, 5)

    doctor_page = request.GET.get('doctor_page')
    patient_page = request.GET.get('patient_page')
    appointment_page = request.GET.get('appointment_page')
    payment_page = request.GET.get('payment_page')

    doctors = doctor_paginator.get_page(doctor_page)
    patients = patient_paginator.get_page(patient_page)
    appointments = appointment_paginator.get_page(appointment_page)
    payments = payment_paginator.get_page(payment_page)

    # STATISTICS
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()
    total_payments = Payment.objects.count()

    total_revenue = 0

    for payment in payments:
        if payment.payment_status == "Paid":
            total_revenue += float(payment.amount)

    return render(
        request,
        'admin_dashboard.html',
        {
            'doctors': doctors,
            'patients': patients,
            'appointments': appointments,
            'payments': payments,
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_payments': total_payments,
            'total_revenue': total_revenue,
        }
    )

from .models import *
from datetime import date
from django.conf import settings
import os


def add_prescription(request, appointment_id):

    appointment = Appointment.objects.get(
        appointment_id=appointment_id
    )

    if request.method == "POST":

        uploaded_file = request.FILES.get(
            'uploaded_file'
        )

        file_name = None

        if uploaded_file:

            upload_dir = os.path.join(
                settings.MEDIA_ROOT,
                'prescriptions'
            )

            os.makedirs(
                upload_dir,
                exist_ok=True
            )

            file_path = os.path.join(
                upload_dir,
                uploaded_file.name
            )

            with open(file_path, 'wb+') as destination:

                for chunk in uploaded_file.chunks():

                    destination.write(chunk)

            file_name = uploaded_file.name

        Prescription.objects.create(

            appointment=appointment,

            doctor=appointment.doctor,

            patient=appointment.patient,

            medication_name=request.POST['medication_name'],

            dosage=request.POST['dosage'],

            frequency=request.POST['frequency'],

            duration=request.POST['duration'],

            notes=request.POST['notes'],

            prescribed_date=date.today(),

            uploaded_file=file_name

        )
        send_mail(
            subject='New Prescription Available',
            message=f'''
        Dear {appointment.patient.user.full_name},

        A prescription has been added by
        Dr. {appointment.doctor.user.full_name}.

        Please login to HIPMS to view it.

        Thank you,
        HIPMS Team
        ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                appointment.patient.user.email
            ],
            fail_silently=True,
        )

        return redirect(
            'doctor_appointments'
        )

    return render(
        request,
        'add_prescription.html',
        {
            'appointment': appointment
        }
    )

def make_payment(request, appointment_id):

    appointment = Appointment.objects.get(
        appointment_id=appointment_id
    )

    if request.method == "POST":

        Payment.objects.create(
            appointment=appointment,
            amount=appointment.doctor.consultation_fee,
            payment_method=request.POST['method'],
            payment_status='Completed',
            transaction_date=request.POST.get('transaction_date')
        )

        return redirect('dashboard')

    return render(
        request,
        'payment.html',
        {
            'appointment': appointment
        }
    )


def download_prescription(request, prescription_id):

    prescription = Prescription.objects.get(
        prescription_id=prescription_id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="Prescription_{prescription_id}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setTitle("Prescription")

    pdf.drawString(100, 800, "Hospital Information & Patient Management System")

    pdf.drawString(100, 760, f"Prescription ID: {prescription.prescription_id}")

    pdf.drawString(100, 730, f"Medicine: {prescription.medication_name}")

    pdf.drawString(100, 700, f"Dosage: {prescription.dosage}")

    pdf.drawString(100, 670, f"Frequency: {prescription.frequency}")

    pdf.drawString(100, 640, f"Duration: {prescription.duration}")

    pdf.drawString(100, 610, f"Notes: {prescription.notes}")

    pdf.save()

    return response

from django.http import FileResponse, Http404
import os

def download_file(request, id):

    prescription = Prescription.objects.get(
        prescription_id=id
    )

    if not prescription.uploaded_file:
        raise Http404("No file attached")

    file_path = prescription.uploaded_file.path

    if not os.path.exists(file_path):
        raise Http404("File not found")

    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True
    )

def hospital_details(request, hospital_id):

    hospital = Hospital.objects.get(
        hospital_id=hospital_id
    )

    doctors = Doctor.objects.filter(
        hospital_id=hospital_id
    )

    patients = Patient.objects.filter(
        hospital_id=hospital_id
    )

    return render(
        request,
        'hospital_details.html',
        {
            'hospital': hospital,
            'doctors': doctors,
            'patients': patients
        }
    )

def hospital_search(request):

    hospitals = Hospital.objects.all()

    return render(
        request,
        'hospital_search.html',
        {
            'hospitals': hospitals
        }
    )

import random

import json

def send_otp(request):

    data = json.loads(request.body)

    phone_no = data.get('phone_no')

    otp = random.randint(100000, 999999)

    request.session['login_otp'] = str(otp)

    print("Entered OTP:", otp)
    print("Stored OTP:", request.session.get('login_otp'))
    return JsonResponse({
        'message': 'OTP Sent'
    })