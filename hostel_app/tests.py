from django.test import TestCase, Client
from .models import HostelProfile
from core.tests import CoreTesting
# Create your tests here.

class HostelTest(CoreTesting):
   
   def setUp(self) -> None:
      return super().setUp()
   

   # def test_hostel_creation(self):
   #    """test hostel creation"""
   #    self.assertTrue(HostelProfile.objects.filter(hostel_code="sk123").exists())

