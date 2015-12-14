__author__ = 'ian'

from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from .models import *
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.forms import ModelForm
import json

# ==================================================================================================
# =========================================== CALENDAR =============================================
# ==================================================================================================
''' Form made for use with the newMessage view '''
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields =['title', 'description', 'date', 'start_time', 'end_time', 'location','patient', 'doctor']

#This is a page that shows either the patient or doctor calendar
@login_required(login_url='/login/')
def get_calendar(request, user, id):
    user_instance = get_object_or_404(User, pk=id)

    create_form = AppointmentForm(request.POST or None)
    message = ""
    try:
        if Patient.objects.get(user=user_instance):
            eventsList = []
            user_type = "patient"
            calendar = Appointment.objects.filter(patient=user_instance)
            item = get_object_or_404(Patient, pk=user)
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
    except Exception as e:
        try:
            if Doctor.objects.get(user=user_instance):
                eventsList = []
                user_type = "doctor"
                calendar = Appointment.objects.filter(doctor=user_instance)
                item = get_object_or_404(Doctor, pk=user)
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
        except Exception as e:
                print(e)
    if create_form.is_valid():
        create_form.save()
        message = "Appointment was created"
        return HttpResponseRedirect('/calendar/%s/%s/' % (user, id))
    return render(request, 'main_site/calendar.html',{'user': user, 'id':id, 'item': item, 'user_type':user_type, 'create_form':create_form, 'message':message, 'eventsList':eventsList })

def parseDate(dateString):
    tempDate = dateString.split("/")
    formatDate = "20" + tempDate[2] + "-" + tempDate[0] + "-" + tempDate[1]
    return formatDate

#Update appointment information
@login_required(login_url='/login/')
def updateAppointment(request, id):
    if request.method == 'GET':
        if request.is_ajax():
            data = Appointment.objects.get(pk=id)
            form_info = {"title":data.title, "description":data.description, "date":data.date, "start":data.start_time, "end":data.end_time}
        return JsonResponse(form_info)
    elif request.method == 'POST':
        if request.is_ajax():
            title = request.POST.get("title")
            description = request.POST.get("description")
            date = request.POST.get("date")
            start = request.POST.get("start")
            end = request.POST.get("end")
            Appointment.objects.filter(pk=id).update(title=title, description=description, date=date, start_time=start, end_time=end)
            # create_event(user_actions[10], request.user, None, None, None) Check how to get user please. Do the same for cancel please.
            return HttpResponseRedirect('')

#delete appointment from doctor profile
@login_required(login_url='/login/')
def cancelAppointment(request, id):
    if request.method == 'DELETE':
        if request.is_ajax():
            Appointment.objects.get(pk=id).delete()
            return HttpResponse("")

def get_doctor_calendar(request):
    if request.method == "GET":
        if request.is_ajax():
            eventsList = []
            item = get_object_or_404(User, pk=request.GET.get("id"))
            if Appointment.objects.filter(doctor=item) == None:
                calendar = None
            else:
                calendar = Appointment.objects.filter(doctor=item)
                for e in calendar:
                    event = {   "title":e.title,
                                "start":parseDate(e.date) + "T"+ e.start_time,
                                "end":parseDate(e.date) + "T"+ e.end_time,
                                "patient":e.patient.username,
                                "description":e.description,
                                "location":e.location.name,
                                "date":parseDate(e.date),
                                "id":e.id,
                                "editable":"true"
                            }
                    eventsList.append(event)
                jsonString = json.dumps(eventsList)
                return HttpResponse(jsonString)