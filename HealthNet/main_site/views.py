from django.shortcuts import get_object_or_404, render
from .models import *
from django.http import *
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

# ==================================================================================================
# =========================================== UPDATE INFO ==========================================
# ==================================================================================================

patientNumber = 0
''' Form made for use with the newMessage view '''
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields =['title', 'description', 'date', 'start_time', 'end_time', 'location','patient', 'doctor']

''' Displays the doctors view of their own profile page '''
@login_required(login_url='/login/')
def doctorDetail(request, user):
    x = check_permissions(["Doctor"], user, request)
    if x != "Success":
        return x

    eventsList = []

    #instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=request.user,urgent='YES')


    item = get_object_or_404(Doctor, pk=user)
    instance = get_object_or_404(User, pk=item.user.id)
    calendar = Appointment.objects.filter(doctor=instance)

    create_form = AppointmentForm(request.POST or None)
    for e in calendar:
        eventsList.append({ 'title':e.title,
                            'start':parseDate(e.date) + "T"+ e.start_time,
                            'end':parseDate(e.date) + "T"+ e.end_time,
                            'patient':e.patient.username,
                            'description':e.description,
                            'location':e.location.name,
                            'date':parseDate(e.date),
                            'id':e.id,
                            'editable':"true"
                            })
    if create_form.is_valid():
        create_form.save()
        return HttpResponseRedirect('/doctors/%s/' % user)
    return render(request, 'main_site/doctorProfile.html', {'item': item,'eventsList':eventsList,'create_form':create_form, 'latest_inbox_list': latest_inbox_list})

''' Displays the nurses view of their own profile page '''
@login_required(login_url='/login/')
def nurseDetail(request, user):
    x = check_permissions(["Nurse"], user, request)
    if x != "Success":
        return x

    eventsList = []
    item = get_object_or_404(Nurse, pk=user)
    create_form = AppointmentForm(request.POST or None)

    #instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=request.user,urgent='YES')


    ##will need to get a list of all doctor calendars
    calendar = Appointment.objects.filter()
    for e in calendar:
        eventsList.append({ 'title':e.title,
                            'start':parseDate(e.date) + "T"+ e.start_time,
                            'end':parseDate(e.date) + "T"+ e.end_time,
                            'patient':e.patient.username,
                            'description':e.description,
                            'location':e.location.name,
                            'date':parseDate(e.date),
                            })
    if create_form.is_valid():
        create_form.save()
    return render(request, 'main_site/nurseProfile.html', {'item': item, 'eventsList':eventsList,'create_form':create_form, 'latest_inbox_list': latest_inbox_list})

''' Displays the patients view of their own profile page '''
@login_required(login_url='/login/')
def patientDetail(request, user):
    x =check_permissions(["Patient"], user, request)
    if x != "Success":
        return x

    eventsList = []


    #instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=request.user,urgent='YES')

    item = get_object_or_404(Patient, pk=user)
    instance = get_object_or_404(User, pk=item.user.id)
    calendar = Appointment.objects.filter(patient=instance)

    create_form = AppointmentForm(request.POST or None)
    for e in calendar:
        eventsList.append({ 'title':e.title,
                            'start':parseDate(e.date) + "T"+ e.start_time,
                            'end':parseDate(e.date) + "T"+ e.end_time,
                            'patient':e.patient.username,
                            'description':e.description,
                            'location':e.location.name,
                            'date':parseDate(e.date),
                            'id':e.id,
                            'editable':"true"
                            })
    if create_form.is_valid():
        create_form.save()
        return HttpResponseRedirect('/patients/%s/' % user)
    return render(request, 'main_site/patientProfile.html', {'item': item, 'eventsList':eventsList, 'create_form':create_form, 'latest_inbox_list': latest_inbox_list})

''' Displays the hospital admins view of their own profile page '''
@login_required(login_url='/login/')
def hospitalAdminDetail(request, user):
    x = check_permissions(["HospitalAdmin"], user, request)
    if x != "Success":
        return x

    eventsList = []
    item = get_object_or_404(HospitalAdmin, pk=user)

    #instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=request.user,urgent='YES')

    ##will need to get a list of all doctor calendars
    calendar = Appointment.objects.filter()
    for e in calendar:
        eventsList.append({ 'title':e.title,
                            'start':parseDate(e.date) + "T"+ e.start_time,
                            'end':parseDate(e.date) + "T"+ e.end_time,
                            'patient':e.patient.username,
                            'description':e.description,
                            'location':e.location.name,
                            'date':parseDate(e.date),
                            })
    return render(request, 'main_site/hospitalAdminProfile.html', {'item': item, 'eventsList':eventsList, 'latest_inbox_list': latest_inbox_list})

def parseDate(dateString):
    tempDate = dateString.split("/")
    formatDate = "20" + tempDate[2] + "-" + tempDate[0] + "-" + tempDate[1]
    return formatDate

''' The form a nurse uses to update a patient '''
@login_required(login_url='/login/')
class NurseUpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('hospital', 'general_practitioner')

''' The page a nurse sees while updating a patient '''
@login_required(login_url='/login/')
def nurse_update_patient(request, user, id):
    x = check_permissions(["Nurse"], user, request)
    if x != "Success":
        return x

    instance = get_object_or_404(Patient, pk=user)
    nurse = get_object_or_404(Nurse, pk=id)
    form = NurseUpdatePatientForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        if new_instance.hospital != None:
            new_instance.hospital.listOfPatients.add(new_instance)
            create_event(user_actions[4], nurse.user, instance.user, None, None)
        return HttpResponseRedirect('/nurses/%s/' % id)
    return render(request, "main_site/update.html", {
        "form" : form,
    })

''' Switches a patients hospital between None and the hospital of the doctor '''
@login_required(login_url='/login/')
def doctor_update_patient_hospital(request, user, id):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    instance = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    if instance.hospital != None:
        instance.hospital = None
        instance.save()
    else:
        instance.hospital = doctor.hospital
        instance.save()
    create_event(user_actions[4], doctor.user, instance.user, doctor.hospital, None)
    return HttpResponseRedirect('/patients-doctor/%s/%s/' % (user,id))

''' The form a doctor uses to update a medical record'''
class UpdateMedForm(ModelForm):
    class Meta:
        model = Record
        fields = ('patient', 'doctor', 'description','result','viewable')

    def is_valid(self):
        return self['description'].value()!=None and self['result'].value()!=None and self['description'].value()!='' and self['result'].value()!=''

''' Adds a medical record to a patient '''
@login_required(login_url='/login/')
def doctor_update_patient_medrecord(request, user, id):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    type = "doctors"
    if request.method == 'POST':
        form = UpdateMedForm(request.POST)
        if form['description'].value() == '' or form['description'].value() == None:
            form = UpdateMedForm(initial={'patient':patient,'doctor':doctor,'description':None,'result':None})
        else:
            form = UpdateMedForm(request.POST)
        if form.is_valid():
            patient.records.add(form.save())
            patient.save()
            create_event(user_actions[18], doctor.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-doctor/%s/%s/' % (user,id))
    elif request.method == 'GET':
        form = UpdateMedForm(initial={'patient':patient,'doctor':doctor,'description':None,'result':None})
    return render(request, "main_site/update.html", {
        "form" : form,"type" : type, "ID" : doctor,
    })

''' The form a Nurse uses to update a medical record'''
class NurseUpdateMedForm(ModelForm):
    class Meta:
        model = Record
        fields = ('patient', 'doctor', 'description','result')

    def is_valid(self):
        return self['description'].value()!=None and self['result'].value()!=None and self['description'].value()!='' and self['result'].value()!=''

''' Adds a medical record to a patient '''
@login_required(login_url='/login/')
def nurse_update_patient_medrecord(request, user, id):
    x = check_permissions(["Nurse"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=user)
    nurse = get_object_or_404(Nurse, pk=id)
    type = "doctors"
    if request.method == 'POST':
        form = NurseUpdateMedForm(request.POST)
        if form['description'].value() == '' or form['description'].value() == None:
            form = NurseUpdateMedForm(initial={'patient':patient,'description':None,'result':None})
        else:
            form = UpdateMedForm(request.POST)
        if form.is_valid():
            patient.records.add(form.save())
            patient.save()
            create_event(user_actions[18], nurse.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-nurse/%s/%s/' % (user,id))
    elif request.method == 'GET':
        form = NurseUpdateMedForm(initial={'patient':patient,'description':None,'result':None})
    return render(request, "main_site/update.html", {
        "form" : form,"type" : type, "ID" : nurse,
    })

''' The form a doctor uses to add a prescription '''
class UpdatePresciptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ('patient', 'doctor', 'medicine','amount','description')

    def is_valid(self):
        return self['medicine'].value()!=None and self['amount'].value()!=None and self['medicine'].value()!='' and self['amount'].value()!=''

''' Switches a patients hospital between None and the hospital of the doctor '''
@login_required(login_url='/login/')
def doctor_update_patient_prescription(request, user, id):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    type = "doctors"
    if request.method == 'POST':
        form = UpdatePresciptionForm(request.POST)
        if form['medicine'].value() == '' or form['medicine'].value() == None:
            form = UpdatePresciptionForm(initial={'patient':patient,'doctor':doctor,'medicine':None,'amount':None})
        else:
            form = UpdatePresciptionForm(request.POST)
        if form.is_valid():
            patient.prescriptions.add(form.save())
            patient.save()
            create_event(user_actions[18], doctor.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-doctor/%s/%s/' % (user,id))
    elif request.method == 'GET':
        form = UpdatePresciptionForm(initial={'patient':patient,'doctor':doctor,'medicine':None,'amount':None})
    return render(request, "main_site/update.html", {
        "form" : form, "ID" : doctor, "type" : type,
    })

''' This is the form a patient sees to update their own information '''
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        exclude = ['user', 'hospital', 'records', 'prescriptions']

''' This is the page a patient sees while updating their information '''
@login_required(login_url='/login/')
def patient_update(request, user):
    x = check_permissions(["Patient"], user, request)
    if x != "Success":
        return x
    instance = get_object_or_404(Patient, pk=user)
    item = PatientForm(request.POST or None, instance=instance)
    type = "patients"
    if item.is_valid():
        new_instance = item.save()
        for nurse in Nurse.objects.all():
            nurse.listOfPatients.remove(instance)
            nurse.listOfPatients.add(new_instance)
        for hospitalAdmin in HospitalAdmin.objects.all():
            hospitalAdmin.listOfPatients.remove(instance)
            hospitalAdmin.listOfPatients.add(new_instance)
        for doctor in Doctor.objects.all():
            doctor.listOfPatients.remove(instance)
            doctor.listOfPatients.add(new_instance)
        create_event(user_actions[3], instance.user, None, None, None)
        return HttpResponseRedirect('/patients/%s/' % instance.id)
    return render(request, "main_site/patientUpdate.html", {
        "item" : instance, "form" : item,
    })

''' This is the form a doctor sees to update their own information '''
class DoctorForm(ModelForm):
    class Meta:
        model = Doctor
        exclude = ['user', 'listOfPatients']

''' This is the page a doctor sees while updating their information '''
@login_required(login_url='/login/')
def doctor_update(request, user):
    x = check_permissions(["Doctor"], user, request)
    if x != "Success":
        return x
    instance = get_object_or_404(Doctor, pk=user)
    previous_hospital = None
   # print instance.id
    if instance.hospital != None:
        previous_hospital = instance.hospital
    form = DoctorForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        if(previous_hospital != None):
            previous_hospital.listOfDoctors.remove(instance)
        if new_instance.hospital != None:
            new_instance.hospital.listOfDoctors.add(new_instance)
        create_event(user_actions[3], instance.user, None, None, None)
        return HttpResponseRedirect('/doctors/%s/' % instance.id)
    return render(request, "main_site/doctorUpdate.html", {
        "form" : form, "item" : instance,
    })

''' This is the form a nurse sees to update their own information '''
class NurseForm(ModelForm):
    class Meta:
        model = Nurse
        exclude = ['user', 'listOfDoctors', 'listOfPatients']

''' This is the page a nurse sees while updating their information '''
@login_required(login_url='/login/')
def nurse_update(request, user):
    x = check_permissions(["Nurse"], user, request)
    if x != "Success":
        return x
    instance = get_object_or_404(Nurse, pk=user)
    previous_hospital = instance.hospital
    form = NurseForm(request.POST or None, instance=instance)
    type = "nurses"
    if form.is_valid():
        new_instance = form.save()
        if(previous_hospital != None):
            previous_hospital.listOfNurses.remove(instance)
        new_instance.hospital.listOfNurses.add(new_instance)
        create_event(user_actions[3], instance.user, None, None, None)
        return HttpResponseRedirect('/nurses/%s/' % instance.id)
    return render(request, "main_site/nurseUpdate.html", {
        "form" : form, "item" : instance, "type" : type,
    })

''' This is the form a hospital administrators sees to update their own information '''
class HospitalAdminForm(ModelForm):
    class Meta:
        model = HospitalAdmin
        exclude = ['user', 'listOfDoctors', 'listOfPatients', 'listOfNurses', 'listOfHospitalAdmins']

''' This is the page a hospital administrator sees while updating their information '''
@login_required(login_url='/login/')
def hospitalAdmin_update(request, user):
    x = check_permissions(["HospitalAdmin"], user, request)
    if x != "Success":
        return x
    instance = get_object_or_404(HospitalAdmin, pk=user)
    previous_hospital = instance.hospital
    form = HospitalAdminForm(request.POST or None, instance=instance)
    if form.is_valid():
        new_instance = form.save()
        if(previous_hospital != None):
            previous_hospital.listOfHospitalAdmins.remove(instance)
        new_instance.hospital.listOfHospitalAdmins.add(new_instance)
        create_event(user_actions[3], instance.user, None, None, None)
        return HttpResponseRedirect('/hospitalAdmins/%s/' % instance.id)
    return render(request, "main_site/adminUpdate.html", {
        "form" : form, "item" : instance,
    })


''' Display a doctors profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def doctorDetail_other(request, user, id):
    x = check_permissions(["HospitalAdmin", "Nurse"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Doctor, pk=user)
    return render(request, 'main_site/userViewingDoctor.html', {'item': item, 'ID': request.user})

''' Display a nurses profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def nurseDetail_other(request, user, id):
    x = check_permissions(["HospitalAdmin"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Nurse, pk=user)
    return render(request, 'main_site/userViewingNurse.html', {'item': item, 'ID': request.user})

''' Display a patients profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def patientDetail_other(request, user, id):
    x = check_permissions(["Doctor", "Nurse", "HospitalAdmin"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Patient, pk=user)
    return render(request, 'main_site/userViewingPatient.html', {'item': item, 'ID': request.user})

''' Display a hospital administrators profile thats being accessed by a different user '''
@login_required(login_url='/login/')
def hospitalAdminDetail_other(request, user, id):
    x = check_permissions(["HospitalAdmin"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(HospitalAdmin, pk=user)
    return render(request, 'main_site/userViewingHospitalAdmin.html', {'item': item, 'ID': request.user})

''' Display a patients profile thats being accessed by a doctor '''
@login_required(login_url='/login/')
def patientDetail_doctor(request, user, id):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Patient, pk=user)
    doctor = get_object_or_404(Doctor, pk=id)
    create_event(user_actions[13], doctor.user, item.user, None, None)
    return render(request, 'main_site/doctorViewingPatient_CanUpdate.html', {'item': item, 'doctor': doctor})

''' Display a patients profile thats being accessed by a hospital administrator '''
@login_required(login_url='/login/')
def patientDetail_admin(request, user, id):
    x = check_permissions(["HospitalAdmin"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Patient, pk=user)
    admin = get_object_or_404(HospitalAdmin, pk=id)
    create_event(user_actions[13], admin.user, item.user, None, None)
    return render(request, 'main_site/userViewingPatient.html', {'item': item, 'ID': request.user})

''' The form that an admin uses to update a patient '''
@login_required(login_url='/login/')
class AdminUpdatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('hospital', 'general_practitioner')

''' Display a patients profile for an administrator that is updating the patient'''
@login_required(login_url='/login/')
def admin_update_patient(request, user, id):
    x = check_permissions(["HospitalAdmin"], user, request)
    if x != "Success":
        return x
    instance = get_object_or_404(Patient, pk=user)
    admin = get_object_or_404(HospitalAdmin, pk=id)
    previous_hospital = instance.hospital
    form = AdminUpdatePatientForm(request.POST or None, instance=instance)
    type = "hospitalAdmins"
    if form.is_valid():
        new_instance = form.save()
        previous_hospital.listOfPatients.remove(instance)
        new_instance.hospital.listOfPatients.add(new_instance)
        if previous_hospital != new_instance.hospital:
            create_event(user_actions[4], admin.user, instance.user, None, None)
        return HttpResponseRedirect('/hospitalAdmins/%s/' % admin.id)
    return render(request, "main_site/update.html", {
        "form" : form, "type" : type, "ID" : admin
    })

''' The patient detail that a nurse sees '''
@login_required(login_url='/login/')
def patientDetail_nurse(request, user, id):
    x = check_permissions(["Nurse"], id, request)
    if x != "Success":
        return x
    item = get_object_or_404(Patient, pk=user)
    nurse = get_object_or_404(Nurse, pk=id)
    create_event(user_actions[13], nurse.user, item.user, None, None)
    if item.hospital == None:
        return render(request, 'main_site/nurseViewingPatient_CanSeeAndUpdate.html', {'item': item, 'nurse':nurse})
    else:
        if item.hospital == nurse.hospital:
            return render(request, 'main_site/nurseViewingPatient_CantUpdate.html', {'item': item})
        else:
            return render(request, 'main_site/nurseViewingPatient_CantSeeOrUpdateInfo.html', {'item': item, 'nurse': nurse})

''' The page not found detail page '''
def page_not_found(request):
    print("Redirecting\n")
    return render(request, 'main_site/pageNotFound.html')

def display_record(request, user, id):
    x = check_permissions(["Doctor", "Nurse", "Patient", "HospitalAdmin"], id, request)
    item = get_object_or_404(Record, pk=user)
    return render(request, "main_site/medRecord.html",{'item': item, 'ID': request.user})

def display_prescriptions(request, user, id):
    x = check_permissions(["Doctor", "Nurse", "Patient", "HospitalAdmin"], id, request)
    item = get_object_or_404(Prescription, pk=user)
    return render(request, "main_site/prescription.html",{'item': item, 'ID': request.user})

def remove_prescription(request, user, id, pat):
    x = check_permissions(["Doctor", "Nurse", "Patient", "HospitalAdmin"], id, request)
    prescription = get_object_or_404(Prescription, pk=user)
    prescription.delete()
    return HttpResponseRedirect('/patients-doctor/%s/%s/' % (pat,id))

@login_required(login_url='/login/')
def doctor_create_patient_prescription(request, user, id, pat):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=pat)
    doctor = get_object_or_404(Doctor, pk=id)
    instance = get_object_or_404(Prescription, pk=user)
    type = "doctors"
    if request.method == 'POST':
        form = UpdatePresciptionForm(request.POST, instance=instance)
        if form['medicine'].value() == '' or form['medicine'].value() == None:
            form = UpdatePresciptionForm(initial={'patient':patient,'doctor':doctor,'medicine':None,'amount':None}, instance=instance)
        else:
            form = UpdatePresciptionForm(request.POST, instance=instance)
        if form.is_valid():
            patient.prescriptions.add(form.save())
            patient.save()
            create_event(user_actions[18], doctor.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-doctor/%s/%s/' % (pat,id))
    elif request.method == 'GET':
        form = UpdatePresciptionForm(initial={'patient':patient,'doctor':doctor,'medicine':None,'amount':None}, instance=instance)
    return render(request, "main_site/update.html", {
        "form" : form, "ID" : doctor, "type" : type,
    })

@login_required(login_url='/login/')
def doctor_create_patient_medrecord(request, user, id, pat):
    x = check_permissions(["Doctor"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=pat)
    doctor = get_object_or_404(Doctor, pk=id)
    instance = get_object_or_404(Record, pk=user)
    type = "doctors"
    if request.method == 'POST':
        form = UpdateMedForm(request.POST, instance=instance)
        if form['description'].value() == '' or form['description'].value() == None:
            form = UpdateMedForm(initial={'patient':patient,'doctor':doctor,'description':None,'result':None}, instance=instance)
        else:
            form = UpdateMedForm(request.POST, instance=instance)
        if form.is_valid():
            patient.records.add(form.save())
            patient.save()
            create_event(user_actions[18], doctor.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-doctor/%s/%s/' % (pat,id))
    elif request.method == 'GET':
        form = UpdateMedForm(initial={'patient':patient,'doctor':doctor,'description':None,'result':None}, instance=instance)
    return render(request, "main_site/update.html", {
        "form" : form,"type" : type, "ID" : doctor,
    })

def doctor_remove_medrecord(request, user, id, pat):
    x = check_permissions(["Doctor", "Nurse", "Patient", "HospitalAdmin"], id, request)
    record = get_object_or_404(Record, pk=user)
    record.delete()
    return HttpResponseRedirect('/patients-doctor/%s/%s/' % (pat,id))

def nurse_remove_medrecord(request, user, id, pat):
    x = check_permissions(["Doctor", "Nurse", "Patient", "HospitalAdmin"], id, request)
    record = get_object_or_404(Record, pk=user)
    record.delete()
    return HttpResponseRedirect('/patients-nurse/%s/%s/' % (pat,id))

@login_required(login_url='/login/')
def nurse_create_patient_medrecord(request, user, id, pat):
    x = check_permissions(["Nurse"], id, request)
    if x != "Success":
        return x
    patient = get_object_or_404(Patient, pk=pat)
    nurse = get_object_or_404(Nurse, pk=id)
    instance = get_object_or_404(Record, pk=user)
    type = "doctors"
    if request.method == 'POST':
        form = NurseUpdateMedForm(request.POST, instance=instance)
        if form['description'].value() == '' or form['description'].value() == None:
            form = NurseUpdateMedForm(initial={'patient':patient,'description':None,'result':None}, instance=instance)
        else:
            form = UpdateMedForm(request.POST, instance=instance)
        if form.is_valid():
            patient.records.add(form.save())
            patient.save()
            create_event(user_actions[18], nurse.user, patient.user, None, None)
            return HttpResponseRedirect('/patients-nurse/%s/%s/' % (pat,id))
    elif request.method == 'GET':
        form = NurseUpdateMedForm(initial={'patient':patient,'description':None,'result':None}, instance=instance)
    return render(request, "main_site/update.html", {
        "form" : form,"type" : type, "ID" : nurse,
    })