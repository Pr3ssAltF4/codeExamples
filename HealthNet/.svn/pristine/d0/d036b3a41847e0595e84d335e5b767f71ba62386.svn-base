__author__ = 'ian'

from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# =================================================================================================
# =========================================== DEFAULT =============================================
# =================================================================================================

''' This redirects people to the login page '''
def default_page(request):
    return render(request, "main_site/landingpage.html")

# ==================================================================================================
# =========================================== LOGIN and LOGOUT =====================================
# ==================================================================================================

''' This is the login page '''
def login_page(request):
    state = "Please Sign In"
    username = password = ""
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            create_event(user_actions[1], User.objects.get(username=username), None, None, None)
            if user.is_active:
                auth.login(request, user)
                state = "You've logged in!"
                all_hospitalAdmins = HospitalAdmin.objects.all()
                for h in all_hospitalAdmins:
                    if username == h.user.username and h.user not in unregistered_hadmins:
                        return HttpResponseRedirect('/hospitalAdmins/%s/' % h.id)
                    else:
                        state = "Your application has not been approved yet"
                all_doctors = Doctor.objects.all()
                for d in all_doctors:
                    if username == d.user.username and d.user not in unregistered_doctors:
                        return HttpResponseRedirect('/doctors/%s/' % d.id)
                    else:
                        state = "Your application has not been approved yet"
                all_nurses = Nurse.objects.all()
                for n in all_nurses:
                    if username == n.user.username and n.user not in unregistered_nurses:
                        return HttpResponseRedirect('/nurses/%s/' % n.id)
                    else:
                        state = "Your application has not been approved yet"
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
    create_event(user_actions[2], request.user, None, None, None)
    auth.logout(request)
    return HttpResponseRedirect('/login/')