from django.test import TestCase, Client
from .models import Booking
from hostel_app.models import HostelProfile
from campus_app.models import CampusProfile
from accounts.models import CustomUser
from rooms_app.models import RoomProfile

# Create your tests here.
class CoreTesting(TestCase):

    def setUp(self) -> None:
        """create campus"""
        # campus_1 = CampusProfile.objects.create(campus_name="knust",campus_code='KNUST', 
        #                                         address="kumasi").save()
        # """create user object"""
        # user_1 = CustomUser.objects.create(first_name="Mike", last_name="Steven", 
        #                 username="Mike_steven",email="lemon@gmail.com", 
        #                 campus=campus_1, password="123", phone="023783728", 
        #                 student_id="90287377",).save()

        # """create hostel"""
        # hostel_1 = HostelProfile.objects.create(hostel_name="sky hostel",hostel_code="sk123",
        #                 category="Homestel🏠",rating=4,
        #                 hostel_id="b909834e-9ce7-4f4d-837b-fccea7ce6c45",
        #                 price_range="3123-3721",number_of_rooms=12,campus=campus_1,
        #                 hostel_manager=user_1,hostel_email="sky@gmail.com",  
        #                 account_number="122435363",
        #                 mobile_money="5537712", manager_contact="13472921",
        #                 location="kumasi", address="paa kumasi")
        
        # """create room"""
        # room_1 = RoomProfile.objects.create(room_no = "sky123", room_id="b909834e-9ce7-4f4d-837b-fccea7ce6c45",campus =campus_1,room_capacity=4, 
        #        hostel = hostel_1,room_price =232.22, room_category='Second Class✅').save()

    # def test_bookin

    def test_display_of_campus_hostel(self):
        """test the display of campus hotels"""
        respond = Client().get("core:index")
        self.assertEqual(respond.status_code, 200)

        """test context of the page"""
        # self.assertEqual(respond.context.get("Campus"), None)

    # def test_campus_creation(self):
    #     """test campus creation"""
    #     self.assertTrue(CampusProfile.objects.get(campus_code="KNUST"))

    # def test_room_creation(self):
    #     """test creation of room"""
    #     self.assertTrue(RoomProfile.objects.get(room_id="b909834e-9ce7-4f4d-837b-fccea7ce6c45"))