
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Problem, Emergency, Token
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import SimpleUploadedFile
import random

# for the image only
from io import BytesIO
from PIL import Image
import os 
from django.conf import settings

def create_image_file():
    
            image = Image.new('RGB', (100, 100), color='red')  # Create a simple red image
            image_file = BytesIO()
            image.save(image_file
            , format='PNG')  # Save as PNG
            image_file.seek(0)  # Go to the beginning of the file
    
    
            return SimpleUploadedFile("test_image.png", image_file.read(), content_type="image/png")

def generate_unique_phone_number(existing_numbers):
    while True:
        # Generate a random phone number (adjust format as needed)
        phone_number = f"+201{random.randint(100000000, 999999999)}"
        if phone_number not in existing_numbers:
            existing_numbers.add(phone_number)
            return phone_number



class TestAPI(APITestCase):
    existing_phone_numbers = set()


    def setUp(self):
        self.unique_phone_number = generate_unique_phone_number(self.existing_phone_numbers)
        self.user = User.objects.create_user(
            phone_number=self.unique_phone_number,
            password="testpass123",
            email="user@example.com",
            username="testuser",
            first_name="test",
            last_name="test",
        )
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.token}"}
    def test_signup(self):
        url = reverse('signup')
        data = {
            "phone_number":    generate_unique_phone_number(self.existing_phone_numbers),
            "password": "testpass123",
            "email": "testuser@example.com",
            "username":"testuser",
            "first_name":"test",
            "last_name":"test",
        }
        response = self.client.post(url, data, format='json')
      
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_login(self):
        url = reverse('login')
        data = {
            "phone_number": self.unique_phone_number,  # Use the generated unique phone number
            "password": "testpass123",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_problem(self):
        url = reverse('create_problem')
       
        photo =  create_image_file()
        data = {
            "coordinates": "40.748817,-73.985428",
            "photo": photo,  # Replace with a valid path or mock
            "user_description": "Test Problem Description"
        }
        response = self.client.post(url, data, format='multipart', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_problem_list(self):
        url = reverse('browse_problems')
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_emergency(self):
        url = reverse('create_emergency')
        photo =  create_image_file()

        data = {
            "coordinates": "40.748817,-73.985428",  # Make sure this matches the expected format
            "photo": photo,  # Use a valid path or mock if required
            "description": "Test Emergency"
        }
        response = self.client.post(url, data, format='multipart', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       


    def test_emergency_list(self):
        url = reverse('browse_emergencies')
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        problem = Problem.objects.create(
        user=self.user,
        coordinates="40.748817,-73.985428",
        user_description="Test Problem Description",
        photo=None  # Set this to a valid photo or mock
    )
        url = reverse('problem_review', args=[problem.id])
        data = {
            "rating": 5,
            "comment": "Great work!"
        }
        response = self.client.post(url, data, format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_profile(self):
        url = reverse('profile')
        data = {
            "email": "newemail@example.com"
        }
        response = self.client.put(url, data, format='json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Profile updated successfully")

    def test_paginated_problem_list(self):
        url = reverse('browse_problems', args=[1])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_paginated_emergency_list(self):
        url = reverse('browse_emergencies', args=[1])
        response = self.client.get(url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        # Delete the test image file if it exists
        test_image_path  = os.path.join(settings.MEDIA_ROOT, "problem_photos", 'test_image.png')
        test_image_path_2= os.path.join(settings.MEDIA_ROOT, "emergency_photos", 'test_image.png')

        if os.path.isfile(test_image_path):

            os.remove(test_image_path)
        if os.path.isfile(test_image_path_2):
            os.remove(test_image_path_2)