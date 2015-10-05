from django.db import models
from django.contrib.auth.models import User

'''Class representing a hospital '''
class Hospital(models.Model):
    """Representation of Hospital in the database"""
    name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 15)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='hospitalDoctors', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='hospitalPatients', blank=True)
    listOfNurses = models.ManyToManyField('Nurse', related_name='hospitalNurses', blank=True)
    listOfHospitalAdmins = models.ManyToManyField('HospitalAdmin', related_name='hospitalAdmins', blank=True)

    def __str__(self):
        """To string def for hospital"""
        return self.name

''' Class that represents a doctor.  Has user as a one to one relationship. '''
class Doctor(models.Model):
    """Representation of Doctor in the database"""
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    ### Not sure if this is relevant or not
    office_location = models.CharField(max_length = 100, null=True)
    hospital = models.ForeignKey('Hospital', default=None, null=True, blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='patients', blank=True)

    def __str__(self):
        """To string def for Doctor"""
        return self.user.get_full_name()

''' Class that represents a nurse.  Has user as a one to one relationship. '''
class Nurse(models.Model):
    """Representation of Nurse in the database"""
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    hospital = models.ForeignKey('Hospital', default=None, null=True)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='doctors', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='patient', blank=True)

    def __str__(self):
        """To string method for Nurse"""
        return self.user.get_full_name()

''' Class that represents a hospital admistrators.  Has user as a one to one relationship. '''
class HospitalAdmin(models.Model):
    """Representation of HospitalAdmin in the database"""
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length = 15, null=True)
    hospital = models.ForeignKey('Hospital', null=True)
    listOfDoctors = models.ManyToManyField('Doctor', related_name='subordinates', blank=True)
    listOfPatients = models.ManyToManyField('Patient', related_name='customers', blank=True)
    listOfNurses = models.ManyToManyField('Nurse', related_name='employees', blank=True)
    listOfHospitalAdmins = models.ManyToManyField('HospitalAdmin', related_name='coworkers', blank=True)

    def __str__(self):
        """To string def for HospitalAdmin"""
        return self.user.get_full_name()

''' Class representing a patient. Uses auth packages' User as a one to one relationship. '''
class Patient(models.Model):
    """Representation of the Patient in the database"""
    user = models.OneToOneField(User)
    address = models.CharField(max_length = 50, null=True)
    phone_number = models.CharField(max_length = 15, null=True)
    initial_medical_info = models.CharField(max_length = 1000, null=True)
    insurance = models.CharField(max_length = 500, null=True)
    gender = models.CharField(max_length = 10, null=True)
    height_in_m = models.FloatField(default=0, null=True)
    weight_in_kg = models.FloatField(default=0, null=True)
    age = models.IntegerField(default=0, null=True)
    emergency_contact = models.ForeignKey('Patient', null=True, blank=True, related_name='emergencyContact')
    new_medical_info = models.CharField(max_length=5000, null=True)
    prescriptions = models.CharField(max_length=5000, null=True)
    hospital = models.ForeignKey('Hospital', null=True, blank=True)
    general_practitioner = models.ForeignKey('Doctor', null=True)

    def __str__(self):
        """To string def for Patient"""
        return self.user.get_full_name()

'''Class representing an appointment '''
class Appointment(models.Model):
    title = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=140, null=True)
    date = models.CharField(max_length=200,null=True)
    start_time = models.CharField(max_length=200,null=True)
    end_time = models.CharField(max_length=200,null=True)
    location = models.ForeignKey('main_site.Hospital', related_name="locs", default="", null=True, blank=True)
    patient = models.ForeignKey(User, related_name="customers", default=None, null=True, blank=True)
    doctor = models.ForeignKey(User, related_name="caretakers", default=None, null=True,blank=True)

    def __str__(self):
        return self.title

'''Class representing a message.  Uses auth packages' User to associate a message with a user'''
class Message(models.Model):
    """Representation of a Message in the database"""
    sender = models.ForeignKey(User, related_name="send", default=None)
    recipient = models.ForeignKey(User, related_name="receive", default=None)
    message_subject = models.CharField("Subject",max_length=25)
    message_text = models.TextField("Message")
    message_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """To string def for Message"""
        return self.message_subject

'''Class representing an event, used for the activity log'''
class Event(models.Model):
    """Representation of an Even in the database. Equivalent to Logging."""
    activity = models.TextField(max_length=500, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """To string method for an event. Like Logging."""
        return self.time + " " + self.activity