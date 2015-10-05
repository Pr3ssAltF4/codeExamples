from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import *
from django.forms import modelform_factory, EmailField, IntegerField, RadioSelect
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import *
from django.forms import ModelForm

patientNumber = 0

''' Displays the doctors view of their own profile page '''
@login_required(login_url='/login/')
def doctorDetail(request, user):
    item = get_object_or_404(Doctor, pk=user)
    return render(request, 'main_site/doctorProfile.html', {'item': item})

''' Displays the nurses view of their own profile page '''
@login_required(login_url='/login/')
def nurseDetail(request, user):
    item = get_object_or_404(Nurse, pk=user)
    return render(request, 'main_site/nurseProfile.html', {'item': item})

''' Displays the patients view of their own profile page '''
@login_required(login_url='/login/')
def patientDetail(request, user):
    item = get_object_or_404(Patient, pk=user)
    return render(request, 'main_site/patientProfile.html', {'item': item})

''' Displays the hospital admins view of their own profile page '''
@login_required(login_url='/login/')
def hospitalAdminDetail(request, user):
    item = get_object_or_404(HospitalAdmin, pk=user)
    return render(request, 'main_site/hospitalAdminProfile.html', {'item': item})

''' Displays the messages the user who received the messages '''
def inbox(request, user):
    instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=instance)
    context = {'latest_inbox_list': latest_inbox_list}
    return render(request, 'main_site/messageInbox.html', context)

''' Displays the messages of the user who sent the messages '''
def outbox(request, user):
    instance = get_object_or_404(User, pk=user)
    latest_outbox_list = Message.objects.filter(sender=instance)
    context = {'latest_outbox_list': latest_outbox_list}
    return render(request, 'main_site/messageOutbox.html', context)

''' Displays the activity log '''
def view_activity_log(request):
    list_of_events = Event.objects.all()
    return render(request, 'main_site/viewLog.html', {'list_of_events': list_of_events})

''' Form made for use with the newMessage view '''
class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude =['message_time_created']

'''View to create a new message.  Redirects user to different page after message has been sent
    depending on the type of user that sent the message.'''
def newMessage(request, user):
    user = get_object_or_404(User, pk=user)
    form = MessageForm(request.POST or None)

    if form.is_valid():
        new_instance = form.save()
        temp = Event(activity='\n' + new_instance.sender.get_full_name() + " sent a message to " + new_instance.recipient.get_full_name())
        temp.save()
        try:
            target = Patient.objects.get(user=user)
            return HttpResponseRedirect('/patients/%s/' % target.id)
        except Exception as e:
            try:
                target = Nurse.objects.get(user=user)
                return HttpResponseRedirect('/nurses/%s/' % target.id)
            except Exception as e:
                try:
                    target = Doctor.objects.get(user=user)
                    return HttpResponseRedirect('/doctors/%s/' % target.id)
                except Exception as e:
                    try:
                        target = HospitalAdmin.objects.get(user=user)
                        return HttpResponseRedirect('/hospitalAdmins/%s/' % target.id)
                    except Exception as e:
                        return render(request, "main_site/update.html", {
                        "form" : form,
                        })

    return render(request, "main_site/update.html", {
        "form" : form,
    })

'''View to see the details of a message once it has been selected from the inbox or outbox.'''
def view_message(request, user):
    item = get_object_or_404(Message, pk=user)
    return render(request, 'main_site/viewMessage.html', {'item': item})

''' Display a doctors profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def doctorDetail_other(request, user):
    item = get_object_or_404(Doctor, pk=user)
    return render(request, 'main_site/notDoctorProfile.html', {'item': item})

''' Display a nurses profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def nurseDetail_other(request, user):
    item = get_object_or_404(Nurse, pk=user)
    return render(request, 'main_site/notNurseProfile.html', {'item': item})

''' Display a patients profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def patientDetail_other(request, user):
    item = get_object_or_404(Patient, pk=user)
    return render(request, 'main_site/notPatientProfile.html', {'item': item})

''' Display a hospital administrators profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def hospitalAdminDetail_other(request, user):
    item = get_object_or_404(HospitalAdmin, pk=user)
    return render(request, 'main_site/notHospitalAdminProfile.html', {'item': item})

''' Display a patients profile thats being accessed by a doctor '''
@login_required(login_url='/login/')
def patientDetail_doctor(request, user, id):
    item = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    temp = Event(activity="\n" + doctor.user.get_full_name() + " viewed the information of " + item.user.get_full_name())
    temp.save()
    return render(request, 'main_site/doctorPatientProfile.html', {'item': item, 'doctor': doctor})

''' Display a patients profile thats being accessed by a hospital administrator '''
def patientDetail_admin(request, user, id):
    item = get_object_or_404(Patient, pk=user)
    admin = get_object_or_404(HospitalAdmin, pk=id)
    temp = Event(activity="\n" + admin.user.get_full_name() + " viewed the information of " + item.user.get_full_name())
    temp.save()
    if item.hospital != None:
        return render(request, 'main_site/adminCanUpdate.html', {'item': item, 'admin': admin})
    else:
        return render(request, 'main_site/notPatientProfile.html', {'item': item})

''' The form that an admin uses to update a patient '''
class AdminUpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('hospital', 'general_practitioner')

''' Display a patients profile for an administrator that is updating the patient'''
@login_required(login_url='/login/')
def admin_update_patient(request, user, id):
    instance = get_object_or_404(Patient, pk=user)
    admin = get_object_or_404(HospitalAdmin, pk=id)
    previous_hospital = instance.hospital
    form = AdminUpdatePatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        previous_hospital.listOfPatients.remove(instance)
        new_instance.hospital.listOfPatients.add(new_instance)
        if previous_hospital != new_instance.hospital:
            temp = Event(activity='\n'+admin.user.get_full_name()+" moved "+new_instance.user.get_full_name()+" from "+previous_hospital.name+" to "+new_instance.hospital.name)
            temp.save()
        return HttpResponseRedirect('/hospitalAdmins/%s/' % admin.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' The patient detail that a nurse sees '''
def patientDetail_nurse(request, user, id):
    item = get_object_or_404(Patient, pk=user)
    nurse = get_object_or_404(Nurse, pk=id)
    temp= Event(activity="\n" + nurse.user.get_full_name() + " viewed the information of " + item.user.get_full_name())
    temp.save()
    if item.hospital == None:
        return render(request, 'main_site/nurseCanUpdate.html', {'item': item, 'nurse':nurse})
    else:
        if item.hospital == nurse.hospital:
            return render(request, 'main_site/nurseCantUpdate.html', {'item': item})
        else:
            return render(request, 'main_site/nurseCantSeeUpdate.html', {'item': item, 'nurse': nurse})

''' The form a nurse uses to update a patient '''
class NurseUpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('hospital', 'general_practitioner')

''' The page a nurse sees while updating a patient '''
@login_required(login_url='/login/')
def nurse_update_patient(request, user, id):
    instance = get_object_or_404(Patient, pk=user)
    nurse = get_object_or_404(Nurse, pk=id)
    form = NurseUpdatePatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        if new_instance.hospital != None:
            new_instance.hospital.listOfPatients.add(new_instance)
            temp = Event(activity="\n"+nurse.user.get_full_name()+" admitted "+instance.user.get_full_name()+" to "+new_instance.hospital.name)
            temp.save()
        return HttpResponseRedirect('/nurses/%s/' % id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' The form a doctor uses to update a patient '''
class DoctorUpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('new_medical_info', 'prescriptions', 'hospital', 'general_practitioner')

''' The page a doctor sees while updating a patient '''
@login_required(login_url='/login/')
def doctor_update_patient(request, user, id):
    instance = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    previous_hospital = None
    if instance.hospital != None:
        previous_hospital = instance.hospital
    form = DoctorUpdatePatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save(commit=False)
        if new_instance.hospital == doctor.hospital:
            if previous_hospital == None:
                temp = Event(activity= "\n"+doctor.user.get_full_name()+" admitted "+instance.user.get_full_name()+" to "+new_instance.hospital.name)
                temp.save()
            else:
                temp = Event(activity= '\n'+doctor.user.get_full_name()+" moved "+new_instance.user.get_full_name()+" from "+previous_hospital.name+" to "+new_instance.hospital.name)
                temp.save()
            form.save()
            if previous_hospital != None:
                previous_hospital.listOfPatients.remove(instance)
            if new_instance.hospital != None:
                new_instance.hospital.listOfPatients.add(new_instance)
            return HttpResponseRedirect('/doctors/%s/' % doctor.id)
        if new_instance.hospital == None and previous_hospital == doctor.hospital:
            form.save()
            temp = Event(activity= "\n"+doctor.user.get_full_name()+" released "+instance.user.get_full_name()+" from "+doctor.hospital.name)
            temp.save()
            if previous_hospital != None:
                previous_hospital.listOfPatients.remove(instance)
            return HttpResponseRedirect('/doctors/%s/' % doctor.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This redirects people to the login page '''
def default_page(request):
    return HttpResponseRedirect('/login/')

''' This is the login page '''
def login_page(request):
    state = "Please log in"
    username = password = ""
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                state = "You've logged in!"
                all_hospitalAdmins = HospitalAdmin.objects.all()
                for h in all_hospitalAdmins:
                    if username == h.user.username:
                        return HttpResponseRedirect('/hospitalAdmins/%s/' % h.id)
                all_doctors = Doctor.objects.all()
                for d in all_doctors:
                    if username == d.user.username:
                        return HttpResponseRedirect('/doctors/%s/' % d.id)
                all_nurses = Nurse.objects.all()
                for n in all_nurses:
                    if username == n.user.username:
                        return HttpResponseRedirect('/nurses/%s/' % n.id)
                all_patients = Patient.objects.all()
                for p in all_patients:
                    if username == p.user.username:
                        return HttpResponseRedirect('/patients/%s/' % p.id)
                return HttpResponseRedirect('/login/')
        else:
            state = "Your username and/or password is incorrect"

    return render(request, "main_site/auth.html", {
        "state":state,
        "username":username,
    })

''' This is the logout page '''
@login_required(login_url='/login/')
def logout_page(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

''' The form used to create a new user '''
class ActorCreationForm(UserCreationForm):
    email = EmailField(required=True)
    #user_type = RadioSelect(, required=True, default=Patient)
    registration_num = IntegerField() # TODO : Should be True. The radio box should be for type of account
    class Meta:
        model=User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email", "registration_num")
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=False)
        user.registration_num=self.cleaned_data["registration_num"]
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user

''' This is the registration page people see to create a new user '''
def registration_page(request):
    if request.POST:
        form = ActorCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if new_user.registration_num == patientNumber:
                new_patient = Patient(user = new_user)
                new_patient.save()
                temp= Event(activity= '\n'+new_patient.user.get_full_name()+" has registered as a patient ")
                temp.save()
                return HttpResponseRedirect('/login/')
            else:
                return HttpResponseRedirect('/login/')
    else:
        form = ActorCreationForm()
    return render(request, "main_site/registration.html", {
        "form":form,
    })

''' This is the form the admin sees to register a doctor '''
class DoctorRegisterForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['listOfPatients']

''' This is the page an administrator sees while registering a doctor '''
@login_required(login_url='/login/')
def register_doctor(request):
    form = DoctorRegisterForm(request.POST or None)
    if form.is_valid():
        new_instance = form.save()
        for patient in Patient.objects.all():
            new_instance.listOfPatients.add(patient)
        for hospitalAdmin in HospitalAdmin.objects.all():
            hospitalAdmin.listOfDoctors.add(new_instance)
        for nurse in Nurse.objects.all():
            nurse.listOfDoctors.add(new_instance)
        new_instance.hospital.listOfDoctors.add(new_instance)
        temp = Event(activity= '\n'+new_instance.user.get_full_name()+" has been registered as a doctor ")
        temp.save()
        return HttpResponseRedirect('/login/')
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form the admin sees to register a nurse '''
class NurseRegisterForm(ModelForm):
    class Meta:
        model = Nurse
        exclude = ['listOfDoctors', 'listOfPatients']

''' This is the page an administrator sees while registering a nurse '''
@login_required(login_url='/login/')
def register_nurse(request):
    form = NurseRegisterForm(request.POST or None)
    if form.is_valid():
        new_instance = form.save()
        new_instance.hospital.listOfNurses.add(new_instance)
        for doctor in Doctor.objects.all():
            new_instance.listOfDoctors.add(doctor)
        for patient in Patient.objects.all():
            new_instance.listOfPatients.add(patient)
        for hospitalAdmin in HospitalAdmin.objects.all():
            hospitalAdmin.listOfNurses.add(new_instance)
        temp= Event(activity= '\n'+new_instance.user.get_full_name()+" has been registered as a nurse ")
        temp.save()
        return HttpResponseRedirect('/login/')
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form the admin sees to register a Hospital Administrator '''
class HospitalAdminRegisterForm(ModelForm):
    class Meta:
        model = HospitalAdmin
        exclude = ['listOfDoctors', 'listOfPatients', 'listOfNurses', 'listOfHospitalAdmins']

''' This is the page an administrator sees while registering a hospital Administrator '''
@login_required(login_url='/login/')
def register_hospitalAdmin(request):
    form = HospitalAdminRegisterForm(request.POST or None)
    if form.is_valid():
        new_instance = form.save()
        for doctor in Doctor.objects.all():
            new_instance.listOfDoctors.add(doctor)
        for patient in Patient.objects.all():
            new_instance.listOfPatients.add(patient)
        for nurse in Nurse.objects.all():
            new_instance.listOfNurses.add(nurse)
        new_instance.hospital.listOfHospitalAdmins.add(new_instance)
        for hospitalAdmin in HospitalAdmin.objects.all():
            hospitalAdmin.listOfHospitalAdmins.add(new_instance)
            new_instance.listOfHospitalAdmins.add(hospitalAdmin)
        temp= Event(activity= '\n'+new_instance.user.get_full_name()+" has been registered as a hospital admin ")
        temp.save()
        return HttpResponseRedirect('/login/')
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form a patient sees to update their own information '''
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'hospital', 'general_practitioner', 'prescriptions', 'new_medical_info']

''' This is the page a patient sees while updating their information '''
@login_required(login_url='/login/')
def patient_update(request, user):
    instance = get_object_or_404(Patient, pk=user)
    form = PatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        for nurse in Nurse.objects.all():
            nurse.listOfPatients.remove(instance)
            nurse.listOfPatients.add(new_instance)
        for hospitalAdmin in HospitalAdmin.objects.all():
            hospitalAdmin.listOfPatients.remove(instance)
            hospitalAdmin.listOfPatients.add(new_instance)
        for doctor in Doctor.objects.all():
            doctor.listOfPatients.remove(instance)
            doctor.listOfPatients.add(new_instance)
        temp= Event(activity= '\n'+new_instance.user.get_full_name()+" has updated their information ")
        temp.save()
        return HttpResponseRedirect('/patients/%s/' % instance.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form a doctor sees to update their own information '''
class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'listOfPatients']

''' This is the page a doctor sees while updating their information '''
@login_required(login_url='/login/')
def doctor_update(request, user):
    instance = get_object_or_404(Doctor, pk=user)
    previous_hospital = None
    if instance.hospital != None:
        previous_hospital = instance.hospital
    form = DoctorForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        previous_hospital.listOfDoctors.remove(instance)
        if new_instance.hospital != None:
            new_instance.hospital.listOfDoctors.add(new_instance)
        temp= Event(activity= '\n'+new_instance.user.get_full_name()+" has updated their information ")
        temp.save()
        return HttpResponseRedirect('/doctors/%s/' % instance.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form a nurse sees to update their own information '''
class NurseForm(ModelForm):
    class Meta:
        model = Nurse
        exclude = ['user', 'listOfDoctors', 'listOfPatients']

''' This is the page a nurse sees while updating their information '''
@login_required(login_url='/login/')
def nurse_update(request, user):
    instance = get_object_or_404(Nurse, pk=user)
    previous_hospital = instance.hospital
    form = NurseForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        previous_hospital.listOfNurses.remove(instance)
        new_instance.hospital.listOfNurses.add(new_instance)
        temp= Event(activity='\n'+new_instance.user.get_full_name()+" has updated their information ")
        temp.save()
        return HttpResponseRedirect('/nurses/%s/' % instance.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' This is the form a hospital administrators sees to update their own information '''
class HospitalAdminForm(ModelForm):
    class Meta:
        model = HospitalAdmin
        exclude = ['user', 'listOfDoctors', 'listOfPatients', 'listOfNurses', 'listOfHospitalAdmins']

''' This is the page a hospital administrator sees while updating their information '''
@login_required(login_url='/login/')
def hospitalAdmin_update(request, user):
    instance = get_object_or_404(HospitalAdmin, pk=user)
    previous_hospital = instance.hospital
    form = HospitalAdminForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        previous_hospital.listOfHospitalAdmins.remove(instance)
        new_instance.hospital.listOfHospitalAdmins.add(new_instance)
        temp= Event(activity= '\n'+new_instance.user.get_full_name()+" has updated their information ")
        temp.save()
        return HttpResponseRedirect('/hospitalAdmins/%s/' % instance.id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })
#This is a page that shows Doctors appointments
def get_appointment_doctor(request, user, id):
    item = get_list_or_404(Appointment, pk=user)
    return render(request, 'main_site/viewAppointmentDoctor.html', {'item': item, "id":id})
#This is a page that shows Patients appointments
def get_appointment_patient(request, user, id):
    item = get_list_or_404(Appointment, pk=user)
    return render(request, 'main_site/viewAppointmentPatient.html', {'item': item, "id":id})

#This is a page that shows Doctor calendar
def get_calendar_doctor(request,user, id):
        instance = get_object_or_404(User, pk=user)
        calendar = Appointment.objects.filter(doctor=instance)
        return render(request, 'main_site/calendarDoctor.html',{'calendar':calendar, 'user': user, "id":id})

#This is a page that shows Patients calendar
def get_calendar_patient(request, user, id):
        instance = get_object_or_404(User, pk=user)
        calendar = Appointment.objects.filter(patient=instance)
        return render(request, 'main_site/calendarPatient.html',{'calendar':calendar, 'user': user, "id":id})

"""def cancel_appointment(request, user, id):
    instance = get_object_or_404(User, pk=user)"""

''' Form made for use with the newMessage view '''
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields =['title', 'description', 'date', 'start_time', 'end_time', 'location','patient', 'doctor']

'''View to create a new message.  Redirects user to different page after message has been sent
    depending on the type of user that sent the message.'''
def newAppointment(request, user, id):
    user = get_object_or_404(User, pk=user)
    form = AppointmentForm(request.POST or None)

    if form.is_valid():
        new_instance = form.save()
        temp = Event(activity='\n' + new_instance.doctor.get_full_name() + " created an appointment for " + new_instance.patient.get_full_name())
        temp.save()
        try:
            target = Patient.objects.get(user=user)
            return HttpResponseRedirect('/patients/%s/' % target.id)
        except Exception as e:
            try:
                target = Nurse.objects.get(user=user)
                return HttpResponseRedirect('/nurses/%s/' % target.id)
            except Exception as e:
                try:
                    target = Doctor.objects.get(user=user)
                    return HttpResponseRedirect('/doctors/%s/' % target.id)
                except Exception as e:
                    try:
                        target = HospitalAdmin.objects.get(user=user)
                        return HttpResponseRedirect('/hospitalAdmins/%s/' % target.id)
                    except Exception as e:
                        return render(request, "main_site/createAppointment.html", {
                        "form" : form,
                        "id":id
                        })

    return render(request, "main_site/createAppointment.html", {
        "form" : form,
        "id":id
    })
"""
def cancelAppointmentPatient(request, user, id):
    instance = get_object_or_404(User, pk=user)
    calendar = Appointment.objects.filter(patient=instance).delete()
    return render(request, "main_site/patientProfile.html", {
        "calendar" : calendar,
        "user": user,
        "id":id
    })

def cancelAppointmentDoctor(request, user, id):
    instance = get_object_or_404(User, pk=user)
    calendar = Appointment.objects.filter(doctor=instance).delete()
    return render(request, "main_site/doctorProfile.html", {
        "calendar" : calendar,
        "user": user,
        "id":id
    })"""