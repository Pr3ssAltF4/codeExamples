
__author__='Tim'

from django.shortcuts import get_object_or_404, render
from .models import Message, Patient, Nurse, create_event, Doctor, HospitalAdmin, user_actions
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.forms import ModelForm

# ==================================================================================================
# ============================================= MESSAGING ==========================================
# ==================================================================================================

'''Choices for whether the message is urgent or not'''
URGENCY = (
    ('YES', 'yes'),
    ('NO', 'no')
)

'''For made for use with the newMessage view'''
class MessageForm(ModelForm):
    urgent = forms.ChoiceField(choices=URGENCY, required=True)
    class Meta:
        model = Message
        widgets = {'sender': forms.HiddenInput()}
        exclude = ['message_time_created']

'''View to create a new message.  Redirects the user to a different page after the message has been sent
depending on the type of user that sent the message.'''
@login_required(login_url='/login/')
def newMessage(request, user):
    user = get_object_or_404(User, pk=user)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_instance = form.save()
            create_event(user_actions[8], User.objects.get(username=request.user), User.objects.get(username=new_instance.recipient), None, None)
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
                            return render(request, "main_site/newMessagePrompt.html",
                                            { "form" : form, "ID" : user})
    elif request.method == 'GET':
        form = MessageForm(initial={'sender':request.user})
    return render(request, "main_site/newMessagePrompt.html",
                  { "form" : form, "ID" : user})

'''View to see the details of a message once it has been selected from the inbox or outbox.'''
@login_required(login_url='/login/')
def view_message(request, user):
    item = get_object_or_404(Message, pk=user)
    return render(request, 'main_site/viewMessage.html', {'item': item, "ID" : request.user})


'''Displays the messages the user has received'''
@login_required(login_url='/login/')
def inbox(request, user):
    create_event(user_actions[9], User.objects.get(username=request.user), None, None, None)
    instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=instance)
    return render(request,'main_site/messagingInbox.html', {'ID': instance, 'latest_inbox_list': latest_inbox_list})

'''Displays the urget messages the user has received'''
@login_required(login_url='/login/')
def urgent_inbox(request, user):
    instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=instance,urgent='YES')
    context = {'latest_inbox_list': latest_inbox_list}
    return render(request,'main_site/messagingInbox.html', context)
'''Displays the non urgent messages the user has received'''
@login_required(login_url='/login/')
def not_urgent_inbox(request, user):
    instance = get_object_or_404(User, pk=user)
    latest_inbox_list = Message.objects.filter(recipient=instance,urgent='NO')
    context = {'latest_inbox_list': latest_inbox_list}
    return render(request,'main_site/messagingInbox.html', context)

'''Displays the messages the user has sent'''
@login_required(login_url='/login/')
def outbox(request, user):
    instance = get_object_or_404(User, pk=user)
    latest_outbox_list = Message.objects.filter(sender=instance)
    context = {'latest_outbox_list': latest_outbox_list}
    return render(request, 'main_site/messagingOutbox.html', context)

@login_required(login_url='/login/')
def deleteMessage(request, user):
    user = get_object_or_404(User, pk=user)
    item = Message.objects.get(pk=user).delete()
    return render(request, "main_site/deleteAppointmentDoctor.html", { "item":item })