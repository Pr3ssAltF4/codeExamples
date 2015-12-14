from django.db import models
from django.contrib.auth.models import User
from django.http import *
from datetime import datetime
from django.shortcuts import get_object_or_404

'''Class representing a hospital '''
class Hospital(models.Model):
    name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 15)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='hospitalDoctors', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='hospitalPatients', blank=True)
    listOfNurses = models.ManyToManyField('Nurse', related_name='hospitalNurses', blank=True)
    listOfHospitalAdmins = models.ManyToManyField('HospitalAdmin', related_name='hospitalAdmins', blank=True)

    def __str__(self):
        return self.name

''' Class that represents a doctor.  Has user as a one to one relationship. '''
class Doctor(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    ### Not sure if this is relevant or not
    office_location = models.CharField(max_length = 100, null=True)
    hospital = models.ForeignKey('Hospital', default=None, null=True, blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='patients', blank=True)

    def __str__(self):
        return self.user.get_full_name()

''' Class that represents a nurse.  Has user as a one to one relationship. '''
class Nurse(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    hospital = models.ForeignKey('Hospital', default=None, null=True)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='doctors', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='patient', blank=True)

    def __str__(self):
        return self.user.get_full_name()

''' Class that represents a hospital admistrators.  Has user as a one to one relationship. '''
class HospitalAdmin(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    hospital = models.ForeignKey('Hospital', null=True)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='subordinates', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='customers', blank=True)
    listOfNurses = models.ManyToManyField('Nurse', related_name='employees', blank=True)
    listOfHospitalAdmins = models.ManyToManyField('HospitalAdmin', related_name='coworkers', blank=True)

    def __str__(self):
        return self.user.get_full_name()

''' Class representing a patient. Uses auth packages' User as a one to one relationship. '''
class Patient(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length = 50, null=True)
    phone_number = models.CharField(max_length = 15, null=True)
    insurance_id = models.CharField(max_length = 500, null=True)
    insurance_provider = models.CharField(max_length=500, null=True)
    gender = models.CharField(max_length = 10, null=True)
    height = models.FloatField(default=0, null=True)
    weight = models.FloatField(default=0, null=True)
    age = models.IntegerField(default=0, null=True)
    emergency_contact = models.ForeignKey('Patient', null=True, blank=True, related_name='emergencyContact')
    hospital = models.ForeignKey('Hospital', null=True, blank=True)
    general_practitioner = models.ForeignKey('Doctor', null=True)
    prescriptions = models.ManyToManyField('Prescription', related_name='prescriptions',blank= True)
    records = models.ManyToManyField('Record', related_name='records',blank=True)

    def __str__(self):
        return self.user.get_full_name()

'''Class representing a prescription for a patient.'''
class Prescription(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    medicine = models.CharField(max_length= 30, null=True)
    amount = models.CharField(max_length= 50, null=True)
    description = models.CharField(max_length= 100, null=True)

    def __str__(self):
        return self.patient.user.get_full_name()

'''Class representing a record for a patient.'''
class Record(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    description = models.CharField(max_length= 500, null=True)
    result = models.CharField(max_length= 500, null=True)
    viewable = models.BooleanField(default=False)
    time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.patient.user.get_full_name()

'''Class representing an appointment '''
class Appointment(models.Model):
    title = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=140, null=True)
    date = models.CharField(max_length=8,null=True)
    start_time = models.CharField(max_length=5,null=True)
    end_time = models.CharField(max_length=5,null=True)
    location = models.ForeignKey('main_site.Hospital', related_name="locs", default="", null=True, blank=True)
    patient = models.ForeignKey(User, related_name="customers", default=None, null=True, blank=True)
    doctor = models.ForeignKey(User, related_name="caretakers", default=None, null=True,blank=True)

    def __str__(self):
        return self.title

'''Choices for whether the message is urgent or not'''
URGENCY = (
    ('YES', 'yes'),
    ('NO', 'no')
)
'''Class representing a message.  Uses auth packaages' User to associate a message with a user'''
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="send")
    recipient = models.ForeignKey(User, related_name="receive", default=None)
    message_subject = models.CharField("Subject", max_length=25)
    message_text = models.TextField("Message")
    message_time_created = models.DateTimeField(auto_now_add=True)
    urgent = models.CharField(max_length=3, choices=URGENCY)
    #field to make message urgent or not

    def __str__(self):
        return self.message_subject

user_actions = [
    "logged in",                    # 0
    "logged out",                   # 1
    "registered as a Patient",      # 2
    "edited profile info",          # 3
    "edited profile info of",       # 4
    "set up an appointment with",   # 5
    "approved the registration of", # 6
    "wrote a message",              # 7
    "viewed the inbox",             # 8
    "updated an appointment",       # 9
    "checked in a patient",         # 10
    "checked out a patient",        # 11
    "viewed activity log",          # 12
    "viewed profile of",            # 13
    "registered as a Doctor",       # 14
    "registered as a Nurse",        # 15
    "registered as an Admin",       # 16
    "registration approved",        # 17
    "added a medical record for",   # 18
    "created a prescription for",   # 19
    "removed a prescription for",   # 20
    "updated a prescription for",   # 21
]

'''Class representing an event, used for the activity log'''
class Event(models.Model):
    activity = models.TextField(max_length=500, blank=True) # an action from the list of actions
    time = models.DateTimeField(auto_now_add=True) # the time of the action in datetime format
    initiated_by = models.ForeignKey(User, related_name="initiator") # the user who initiated the action
    target_of = models.ForeignKey(User, default = None, related_name="target", null = True) # the user who is the target of the action
    hospitals = models.ForeignKey(Hospital, default=None, null = True)
    prescriptions = models.ForeignKey(Prescription, default=None, null = True)

    def __str__(self):
        if self.target_of == None:
            return str(self.time) + " " + self.initiated_by.username + " " + str(self.activity)
        return str(self.time) + " " + self.initiated_by.username + " " + str(self.activity) + " " + self.target_of.username

''' Creates an event object and saves it with the appropriate attributes. '''
def create_event(action, init, target, hospital, prescription):
    event = Event(activity = action, initiated_by = init, target_of = target, hospitals = hospital, prescriptions = prescription)
    event.save()

unregistered_nurses = []
unregistered_doctors = []
unregistered_hadmins = []

''' Checks for permissions and redirects if not approved. '''
def check_permissions(expected_types, user, request):
    print("Checking\n")
    print(type(request.user))
    print(request.user.id)
    id_expected =  User.objects.get(id=request.user.id).id
    if "Doctor" in expected_types:
        try:
            print("Checking for doctor\n")
            is_doctor = get_object_or_404(Doctor, pk=user)
            if id_expected != is_doctor.user.id:
                raise Exception
            return "Success"
        except Exception as e:
            print("not a doctor")
    if "Nurse" in expected_types:
        try:
            print("Checking for nurse\n")
            is_nurse = get_object_or_404(Nurse, pk=user)
            if id_expected != is_nurse.user.id:
                raise Exception
            return "Success"
        except Exception as e:
            print("not a nurse")
    if "Patient" in expected_types:
        try:
            print("Checking for patient\n")
            is_patient = get_object_or_404(Patient, pk=user)
            print("Got here")
            if id_expected != is_patient.user.id:
                raise Exception
            return "Success"
        except Exception as e:
            print("not a patient")
    if "HospitalAdmin" in expected_types:
        try:
            print("Checking for hadmin\n")
            is_hadmin = get_object_or_404(HospitalAdmin, pk=user)
            if id_expected != is_hadmin.user.id:
                raise Exception
            return "Success"
        except Exception as e:
            print("not an admin")
    print("Redirecting!\n")
    return HttpResponseRedirect("/page-not-found/")

def export_csv():
    print("Starting DB export script...\n")
    print("Creating csv file 'csv_output.csv'...\n")
    with open('csv_output.csv', 'w+') as file:
        print("Writing out Patients...\n")
        for p in Patient.objects.all():
            file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,\n"
                   % ("Patient", p.user.username, p.user.password, p.user.first_name, p.user.last_name, p.hospital.name, p.insurance_provider, p.insurance_id, "nil"))
        print("Writing out Doctors...\n")
        for d in Doctor.objects.all():
            file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,\n"
                   % ("Doctor", d.user.username, d.user.password, d.user.first_name, d.user.last_name, d.hospital.name, "nil","nil","nil"))
        print("Writing out Nurses...\n")
        for n in Nurse.objects.all():
            file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,\n"
                   % ("Nurse", n.user.username, n.user.password, n.user.first_name, n.user.last_name, n.hospital.name, "nil", "nil", "nil"))
        print("Writing out Hospital Admins...\n")
        for ha in HospitalAdmin.objects.all():
            file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,\n"
                   % ("HospitalAdmin", ha.user.username, ha.user.password, ha.user.first_name, ha.user.last_name, ha.hospital.name, "nil", "nil", "nil"))
        print("Finished creating csv.\n")