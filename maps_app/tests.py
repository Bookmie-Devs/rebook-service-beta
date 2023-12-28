from django.test import TestCase, Client

# Create your tests here.

class MapTest(TestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    

    def test_map_display(self):
        """check if map direction has been diplayed"""
        test_user = Client().get("maps:hostel-direction")
        self.assertEqual(test_user.status_code, 200)

    
    def display_of_map_views(self):
        """check display of hostel map views"""
        test_user = Client().get("maps:map-views")
        self.assertEqual(test_user.status_code, 200)

