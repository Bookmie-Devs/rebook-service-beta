from django.test import TestCase
from django.urls import reverse, resolve
from .models import Booking
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from accounts.models import CustomUser
from rooms_app.models import RoomProfile

# Create your tests here.
class CoreTesting(TestCase):

    def test_index_page(self):
        """Test the display of index page"""
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<span> Modern</span>")

    def test_index_correct_url(self):
        """Test index page with correct url"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<title>Bookmie.com | Booking and Paying for Hostels Just Got Easy with Bookmie.com</title>")

    def test_about_page(self):
        """Test about page"""
        response2 = self.client.get('/about/')
        self.assertEqual(response2.status_code, 200)
        # name urls
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "<b>Easy Booking Process:</b>")

