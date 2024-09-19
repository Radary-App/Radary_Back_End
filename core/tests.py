from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import User 

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class SignUpViewTest(APITestCase):

    def setUp(self):
        # This method is used to set up any pre-test conditions if needed
        self.url = reverse('signup')  # Replace 'signup' with the actual URL name for the SignUpView

    def test_signup_success(self):
        # Define the test data for a successful signup
        test_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword',
            'email': 'johndoe@example.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01',
            'governorate': 'Cairo',
            'markaz': 'Nasr City'
        }

        # Perform the POST request
        response = self.client.post(self.url, test_data, format='json')

        # Check if the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

        # Check if the user was created in the database
        user = User.objects.filter(email='johndoe@example.com').exists()
        self.assertTrue(user)

    def test_signup_invalid_data(self):
        # Define invalid test data (missing required fields, etc.)
        invalid_data = {
            'first_name': '',  # Invalid data
            'last_name': 'Doe',
            'password': 'password',
            'email': '',  # Missing email
        }

        # Perform the POST request
        response = self.client.post(self.url, invalid_data, format='json')

        # Check if the response status code is 400 (bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)  # Check that email validation failed


class AuthenticatedViewTestCase(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = Client()

    def test_authenticated_post_request(self):
        # Log in the user
        self.client.login(phone_number='12345678902', password='strongpassword')
        
        # Define the URL and POST data
        url = '/problem/create/'
        post_data = {
            'field1': 'value1',
            'field2': 'value2',
            # Add other fields as needed
        }
        
        # Make the POST request
        response = self.client.post(url, data=post_data, content_type='application/json')
        
        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Or another expected status code
        
        # Optionally, you can assert the response content
        # self.assertEqual(response.json(), {'expected': 'response'})















































# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Report, AI, Token
# from rest_framework.test import APIClient
# from rest_framework.utils import json
# from django.utils.crypto import get_random_string
# User = get_user_model()

# class UserModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', 
#             username='testuser', 
#             password='password123'
#         )

#     def test_user_creation(self):
#         self.assertEqual(self.user.username, 'testuser')
#         self.assertTrue(self.user.check_password('password123'))

# class ReportModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', 
#             username='testuser', 
#             password='password123'
#         )
#         self.issue = Report.objects.create(
#             title='Test Issue',
#             description='This is a test issue',
#             address='Test Address',
#             level='medium',
#             user=self.user
#         )

#     def test_issue_creation(self):
#         self.assertEqual(self.issue.title, 'Test Issue')
#         self.assertEqual(self.issue.level, 'medium')

# class AIModelTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', 
#             username='testuser', 
#             password='password123'
#         )
#         self.issue = Report.objects.create(
#             title='Test Issue',
#             description='This is a test issue',
#             address='Test Address',
#             level='medium',
#             user=self.user
#         )
#         self.ai = AI.objects.create(
#             issue=self.issue,
#             ai_description='AI generated description',
#             ai_solution='AI generated solution',
#             ai_danger_level='medium'
#         )

#     def test_ai_creation(self):
#         self.assertEqual(self.ai.ai_description, 'AI generated description')
#         self.assertEqual(self.ai.ai_solution, 'AI generated solution')


# class ReportListViewTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(
#             email='test@example.com', 
#             username='testuser', 
#             password='password123'
#         )

#         self.token = get_random_string(255)
#         Token.objects.create(user=self.user, token=self.token)

#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

#     def test_issue_list_view(self):

#         Report.objects.create(title='Test Report', address='Test Address', level='low', user=self.user)
#         response = self.client.get('/reports/')
#         response_data = response.json()
        
#         # Debugging: Print response details
#         print('Status Code:', response.status_code)
#         print('Response Data:', response_data)
        
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Test Report', [item['title'] for item in response_data])