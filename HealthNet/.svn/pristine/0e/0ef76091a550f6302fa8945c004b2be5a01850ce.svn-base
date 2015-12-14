from django.conf.urls import url
from . import login_and_landing_views, registration_views, patient_views, doctor_views, nurse_views, hosp_admin_views, \
    views, calendar_views, messaging_views, log_views

"""URLs used by the views in main_site."""
urlpatterns = [
    # Something???
    url(r'^doctors/(?P<user>[0-9]+)/', views.doctorDetail, name='doctorDetail'),
    url(r'^patients/(?P<user>[0-9]+)/', views.patientDetail, name='patientDetail'),
    url(r'^nurses/(?P<user>[0-9]+)/', views.nurseDetail, name='nurseDetail'),
    url(r'^hospitalAdmins/(?P<user>[0-9]+)/', views.hospitalAdminDetail, name='hospitalAdminDetail'),
    url(r'^doctors-other/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.doctorDetail_other, name='doctorDetail_other'),
    url(r'^patients-other/(?P<user>[0-9]+)/', views.patientDetail_other, name='patientDetail_other'),
    url(r'^patients-admin/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.patientDetail_admin, name='patientDetail_admin'),
    url(r'^nurses-other/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.nurseDetail_other, name='nurseDetail_other'),
    url(r'^hospitalAdmins-other/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.hospitalAdminDetail_other, name='hospitalAdminDetail_other'),
    url(r'^patients-doctor/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.patientDetail_doctor, name='patientDetail_doctor'),
    url(r'^patients-nurse/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.patientDetail_nurse, name='patientDetail_nurse'),
    url(r'^doctor-updates-patient-hospital/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.doctor_update_patient_hospital, name='doctor_update_patient'),
    url(r'^doctor-updates-patient-prescription/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.doctor_update_patient_prescription, name='doctor_update_patient'),
    url(r'^doctor-updates-patient-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.doctor_update_patient_medrecord, name='doctor_update_patient'),
    url(r'^nurse-updates-patient-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.nurse_update_patient_medrecord, name='nurse_update_patient'),
    url(r'^admin-updates-patient/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.admin_update_patient, name='admin_update_patient'),
    url(r'^nurse-updates-patient/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.nurse_update_patient, name='nurse_update_patient'),
    url(r'^med-record/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.display_record, name='display_record'),
    url(r'^prescriptions/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', views.display_prescriptions, name='display_prescriptions'),
    url(r'^remove-prescription/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.remove_prescription, name='remove_prescription'),
    url(r'^doctor-creates-patient-prescription/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.doctor_create_patient_prescription, name='doctor_update_patient'),
    url(r'^doctor-creates-patient-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.doctor_create_patient_medrecord, name='doctor_update_patient'),
    url(r'^nurse-creates-patient-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.nurse_create_patient_medrecord, name='doctor_update_patient'),
    url(r'^nurse-remove-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.nurse_remove_medrecord, name='doctor_update_patient'),
    url(r'^doctor-remove-medrecord/(?P<user>[0-9]+)/(?P<id>[0-9]+)/(?P<pat>[0-9]+)/', views.doctor_remove_medrecord, name='doctor_update_patient'),
    # Messaging
    url(r'^inbox/(?P<user>[0-9]+)/', messaging_views.inbox, name='inbox'),
    url(r'^outbox/(?P<user>[0-9]+)/', messaging_views.outbox, name='outbox'),
    url(r'^message/(?P<user>[0-9]+)/', messaging_views.newMessage, name='newMessage'),
    url(r'^view-message/(?P<user>[0-9]+)/', messaging_views.view_message, name='view_message'),
    url(r'^delete-message/(?P<user>[0-9]+)/', messaging_views.deleteMessage, name='deleteMessage'),

    # System stats and activity log
    url(r'^view-log/(?P<user>[0-9]+)/', log_views.view_activity_log, name='view_activity_log'),
    url(r'^unregistered-personnel/(?P<user>[0-9]+)/', registration_views.unregistered_personnel_list, name='unregistered personnel'),

    # login, logout, and landing page
    url(r'^login/$', login_and_landing_views.login_page, name='Login'),
    url(r'^logout/$', login_and_landing_views.logout_page, name="Logout"),
    url(r'^$', login_and_landing_views.default_page, name="default_page"),

    # registration
    url(r'^registration/$', registration_views.registration, name='Registration'),

    # admin confirm registration
    url(r'^register-doctor/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', registration_views.register_doctor, name='register_doctor'),
    url(r'^register-hospitalAdmin/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', registration_views.register_hospitalAdmin, name='register_hospitalAdmin'),
    url(r'^register-nurse/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', registration_views.register_nurse, name='register_nurse'),

    # update profile info
    url(r'^patient-update/(?P<user>[0-9]+)/', views.patient_update, name='patient_update'),
    url(r'^doctor-update/(?P<user>[0-9]+)/', views.doctor_update, name='doctor_update'),
    url(r'^nurse-update/(?P<user>[0-9]+)/', views.nurse_update, name='nurse_update'),
    url(r'^hospitalAdmin-update/(?P<user>[0-9]+)/', views.hospitalAdmin_update, name='hospitalAdmin_update'),

    # Calendar
    url(r'^calendar/(?P<user>[0-9]+)/(?P<id>[0-9]+)/', calendar_views.get_calendar, name='get_calendar'),
    url(r'^update-appointment/(?P<id>[0-9]+)/', calendar_views.updateAppointment, name='updateAppointment'),
    url(r'^cancel-appointment/(?P<id>[0-9]+)/', calendar_views.cancelAppointment, name='cancelAppointment'),
    url(r'^doctor-calendars/', calendar_views.get_doctor_calendar, name='get_calendar_doctors'),

    # 404 page
    url(r'^page-not-found/', views.page_not_found, name='404 page'),
]