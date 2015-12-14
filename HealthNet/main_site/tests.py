from django.test import TestCase
from .models import *

class DoctorTestCase(TestCase):
    def setUp(self):
        Doctor.objects.create()

    def test_doctor_returns_name(self):
        joeBob = Doctor.objects.get()
        self.assertEqual(joeBob.__str__(), "Joe Bob")