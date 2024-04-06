from django.test import TestCase
from django.urls import reverse
from campus_app.models import CampusProfile
from accounts.models import CustomUser, Student

# Create your tests here.

class TestAccounts(TestCase):
    def setUp(self) -> None:

        """create campus"""
        campus = CampusProfile.objects.create(
                    campus_name="knust",
                    campus_code='KNUST', 
                    address="kumasi"
                    )
        campus.save()
    
        user = CustomUser.objects.create(
                first_name="Mike", 
                last_name="Steven", 
                username="Mike_steven",
                email="lemsaon@gmail.com", 
                password="123",
                phone="023783728", 
                )
        user.save()

        student = Student.objects.create(
                        user=user,
                        student_id_number="3747482",
                        campus=campus
                        )
        student.save()

    def test_user_creation(self):
        """test user creation"""
        self.assertTrue(CustomUser.objects.filter(email="lemsaon@gmail.com").exists())
    
    def test_student_model(self):
        self.assertTrue(Student.objects.filter(student_id_number=3747482).exists())

    def test_url_existance_at_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_url_exixstance_by_name(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        response_2 = self.client.get(reverse('accounts:login'))
        self.assertEqual(response_2.status_code, 200)
        self.assertContains(response_2, "<title>Log in | Sign in to Your Bookmie Profile</title>")
