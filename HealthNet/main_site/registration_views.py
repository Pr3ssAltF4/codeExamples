from .models import *
from django.forms import  EmailField, IntegerField, CharField
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render

# ==================================================================================================
# =========================================== REGISTRATION =========================================
# ==================================================================================================

# Patient
''' The form used to create a new patient user '''
class PatientCreationForm(UserCreationForm):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    insurance_id = CharField(required=True)
    insurance_provider = CharField(required=True)

    class Meta:
        model=User
        fields = ("username" ,"password1", "password2")

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
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.insurance_id = self.cleaned_data["insurance_id"]
        user.insurance_provider = self.cleaned_data["insurance_provider"]
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user

# Medical Personnel
''' Form used in medical personnel registration. Extends UserCreationForm '''
class MedicalPersonnelCreationForm(UserCreationForm):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    choices = (
        (Nurse, 'Nurse'),
        (Doctor, 'Doctor'),
        (HospitalAdmin, 'Admin'),
    )
    position = forms.ChoiceField(choices = choices)
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
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
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        # position = self.cleaned_data['choices']
        user.set_password(self.clean_password2())
        if commit:
            user.save()
        return user

def registration(request):
    if request.method == 'POST':
        form1 = PatientCreationForm(request.POST)
        form2 = MedicalPersonnelCreationForm(request.POST)
        if form1.is_valid():
            new_patient_user = form1.save()
            new_patient = Patient(user = new_patient_user,
                                  insurance_id= form1.cleaned_data['insurance_id'],
                                  insurance_provider = form1.cleaned_data['insurance_provider'],
                                  )
            new_patient.save()
            for doctor in Doctor.objects.all():
                if doctor != None:
                    doctor.listOfPatients.add(new_patient)
            for nurse in Nurse.objects.all():
                if nurse != None:
                    nurse.listOfPatients.add(new_patient)
            for hospitalAdmin in HospitalAdmin.objects.all():
                if hospitalAdmin != None:
                    hospitalAdmin.listOfPatients.add(new_patient)
            create_event(user_actions[3], new_patient.user, None, None, None)
            return HttpResponseRedirect('/login/')
        if form2.is_valid():
            new_personnel_user = form2.save()
            ##DONOT change the conditional because the value of the choice is formatted like this in returned form in the template
            if form2.cleaned_data['position'] == "<class 'main_site.models.Nurse'>":
                new_nurse = Nurse(user = new_personnel_user)
                new_nurse.save()
                unregistered_nurses.append(new_nurse.user)
                for doctor in Doctor.objects.all():
                    if doctor != None:
                        new_nurse.listOfDoctors.add(doctor)
                for patient in Patient.objects.all():
                    if patient != None:
                        new_nurse.listOfPatients.add(patient)
                for hospitalAdmin in HospitalAdmin.objects.all():
                    if hospitalAdmin != None:
                        hospitalAdmin.listOfNurses.add(new_nurse)
                create_event(user_actions[16], new_nurse.user, None, None, None)
            elif form2.cleaned_data['position'] == "<class 'main_site.models.Doctor'>":
                new_doctor = Doctor(user = new_personnel_user)
                new_doctor.save()
                unregistered_doctors.append(new_doctor.user)
                for patient in Patient.objects.all():
                    if patient != None:
                        new_doctor.listOfPatients.add(patient)
                for hospitalAdmin in HospitalAdmin.objects.all():
                    if hospitalAdmin != None:
                        hospitalAdmin.listOfDoctors.add(new_doctor)
                for nurse in Nurse.objects.all():
                    if nurse != None:
                        nurse.listOfDoctors.add(new_doctor)
                create_event(user_actions[15], new_doctor.user, None, None, None)
            else:
                new_hadmin = HospitalAdmin(user = new_personnel_user)
                new_hadmin.save()
                unregistered_hadmins.append(new_hadmin.user)
                for doctor in Doctor.objects.all():
                    if doctor != None:
                        new_hadmin.listOfDoctors.add(doctor)
                for patient in Patient.objects.all():
                    if patient != None:
                        new_hadmin.listOfPatients.add(patient)
                for nurse in Nurse.objects.all():
                    if nurse != None:
                        new_hadmin.listOfNurses.add(nurse)
                for hospitalAdmin in HospitalAdmin.objects.all():
                    hospitalAdmin.listOfHospitalAdmins.add(new_hadmin)
                    new_hadmin.listOfHospitalAdmins.add(hospitalAdmin)
                create_event(user_actions[17], new_hadmin.user, None, None, None)
            return HttpResponseRedirect('/login/')
    else:
        form1 = PatientCreationForm()
        form2 = MedicalPersonnelCreationForm()
    return render(request, "main_site/registration.html", {
        "form1" :form1,
        "form2":form2
    })



# ==================================================================================================
# =========================================== ADMIN REGISTERATION APPROVAL =========================
# ==================================================================================================

# a dictionary containing the usernames of all registered personnel
currently_registered_personnel = {}

''' This is the form the admin sees to register a doctor '''
class DoctorRegisterForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['listOfPatients']

''' This is the page an administrator sees while registering a doctor '''
@login_required(login_url='/login/')
def register_doctor(request, user, id):
    item = get_object_or_404(User, pk=user)
    unregistered_doctors.remove(item)
    return HttpResponseRedirect('/hospitalAdmins/%s/' %id)

''' This is the form the admin sees to register a nurse '''
class NurseRegisterForm(ModelForm):
    class Meta:
        model = Nurse
        exclude = ['listOfDoctors', 'listOfPatients']

''' This is the page an administrator sees while registering a nurse '''
@login_required(login_url='/login/')
def register_nurse(request, user, id):
    item = get_object_or_404(User, pk=user)
    unregistered_nurses.remove(item)
    return HttpResponseRedirect('/hospitalAdmins/%s/' %id)


''' This is the form the admin sees to register a Hospital Administrator '''
class HospitalAdminRegisterForm(ModelForm):
    class Meta:
        model = HospitalAdmin
        exclude = ['listOfDoctors', 'listOfPatients', 'listOfNurses', 'listOfHospitalAdmins']

''' This is the page an administrator sees while registering a hospital Administrator '''
@login_required(login_url='/login/')
def register_hospitalAdmin(request, user, id):
    item = get_object_or_404(User, pk=user)
    unregistered_hadmins.remove(item)
    return HttpResponseRedirect('/hospitalAdmins/%s/' %id)

@login_required(login_url='/login/')
def unregistered_personnel_list(request, user):
    item = get_object_or_404(HospitalAdmin, pk=user)
    return render(request, 'main_site/unregisteredUsers.html', {
        'unregistered_nurses' : unregistered_nurses,
        'unregistered_doctors' : unregistered_doctors,
        'unregistered_hadmins' : unregistered_hadmins,
        'item' : item,
    })