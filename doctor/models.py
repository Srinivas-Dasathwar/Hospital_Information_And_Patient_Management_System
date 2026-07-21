# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appointment(models.Model):

    appointment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        'Patient',
        models.DO_NOTHING
    )

    doctor = models.ForeignKey(
        'Doctor',
        models.DO_NOTHING
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.CharField(
        max_length=100
    )

    medical_file = models.FileField(
        upload_to='medical_reports/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    class Meta:
        managed = False
        db_table = 'appointment'


class AppointmentAppointments(models.Model):
    id = models.BigAutoField(primary_key=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20)
    doctor = models.ForeignKey('DoctorDoctors', models.DO_NOTHING)
    patient = models.ForeignKey('PatientPatients', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appointment_appointments'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        'Users',
        models.DO_NOTHING
    )

    hospital = models.ForeignKey(
        'Hospital',
        models.DO_NOTHING,
        blank=True,
        null=True
    )

    full_name = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    qualification = models.CharField(max_length=100)

    experience_years = models.IntegerField()

    consultation_fee = models.IntegerField()

    availability = models.CharField(max_length=100)

    photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class DoctorDoctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    fee = models.IntegerField()
    user = models.OneToOneField('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'doctor_doctors'


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        'Users',
        models.DO_NOTHING
    )

    hospital = models.ForeignKey(
        'Hospital',
        models.DO_NOTHING,
        blank=True,
        null=True
    )

    full_name = models.CharField(max_length=100)

    blood_group = models.CharField(max_length=100)

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    medical_history = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'

class PatientPatients(models.Model):
    id = models.BigAutoField(primary_key=True)
    blood_group = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.TextField()
    user = models.OneToOneField('UsersUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patient_patients'



class Prescription(models.Model):

    prescription_id = models.AutoField(
        primary_key=True
    )

    appointment = models.ForeignKey(
        Appointment,
        models.DO_NOTHING,
        db_column='appointment_id'
    )

    doctor = models.ForeignKey(
        Doctor,
        models.DO_NOTHING,
        db_column='doctor_id'
    )

    patient = models.ForeignKey(
        Patient,
        models.DO_NOTHING,
        db_column='patient_id'
    )

    medication_name = models.CharField(
        max_length=100
    )

    dosage = models.CharField(
        max_length=50
    )

    frequency = models.CharField(
        max_length=50
    )

    duration = models.CharField(
        max_length=50
    )

    notes = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    prescribed_date = models.DateField()


    uploaded_file = models.FileField(
        upload_to='prescriptions/',
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'prescription'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    phone_no = models.BigIntegerField(unique=True)
    gender = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'users'


class UsersUsers(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=254)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'users_users'



class Payment(models.Model):

    payment_id = models.AutoField(
        primary_key=True
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        db_column='appointment_id'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20
    )

    transaction_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'PAYMENT'


class Hospital(models.Model):

    hospital_id = models.AutoField(
        primary_key=True
    )

    hospital_name = models.CharField(
        max_length=200
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    class Meta:
        managed = False
        db_table = 'hospital'