from django.test import TestCase, Client
from campus_app.models import CampusProfile
from accounts.models import CustomUser

# Create your tests here.

class TestUser(TestCase):

    def setUp(self) -> None:
        """create campus"""
        campus_1 = CampusProfile.objects.create(campus_name="knust",campus_code='KNUST', 
                                                address="kumasi")
        """create user object"""
        user_1 = CustomUser.objects.create(first_name="Mike", last_name="Steven", 
                        username="Mike_steven",email="lemon@gmail.com", 
                        campus=campus_1, 
                        password="123", phone="023783728", 
                        student_id="90287377",).save()
    
    def test_user_creation(self):
        """test user creation"""
        self.assertTrue(CustomUser.objects.filter(username="Mike_steven").exists())