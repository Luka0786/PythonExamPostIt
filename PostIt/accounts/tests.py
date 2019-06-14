from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class TestViewUrls(TestCase):
    def setUp(self):
        #Some urls needs a user to be logged in otherwise we cant access them
        self.user = User.objects.create(username="testUserName")
        self.user.set_password("testPassword")
        self.user.save()
        self.client.force_login(self.user)
    
    def test_view_url_exists_at_location_signup(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

        
    def test_view_url_exists_at_location_profile(self):
       
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_location_profile_edit(self):
        response = self.client.get('/accounts/profile/edit')
        self.assertEqual(response.status_code, 200)

