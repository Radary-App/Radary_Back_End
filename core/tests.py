from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Report, AI, Token
from rest_framework.test import APIClient
from rest_framework.utils import json
from django.utils.crypto import get_random_string
User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', 
            username='testuser', 
            password='password123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('password123'))

class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', 
            username='testuser', 
            password='password123'
        )
        self.issue = Report.objects.create(
            title='Test Issue',
            description='This is a test issue',
            address='Test Address',
            level='medium',
            user=self.user
        )

    def test_issue_creation(self):
        self.assertEqual(self.issue.title, 'Test Issue')
        self.assertEqual(self.issue.level, 'medium')

class AIModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', 
            username='testuser', 
            password='password123'
        )
        self.issue = Report.objects.create(
            title='Test Issue',
            description='This is a test issue',
            address='Test Address',
            level='medium',
            user=self.user
        )
        self.ai = AI.objects.create(
            issue=self.issue,
            ai_description='AI generated description',
            ai_solution='AI generated solution',
            ai_danger_level='medium'
        )

    def test_ai_creation(self):
        self.assertEqual(self.ai.ai_description, 'AI generated description')
        self.assertEqual(self.ai.ai_solution, 'AI generated solution')


class ReportListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', 
            username='testuser', 
            password='password123'
        )

        self.token = get_random_string(255)
        Token.objects.create(user=self.user, token=self.token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_issue_list_view(self):

        Report.objects.create(title='Test Report', address='Test Address', level='low', user=self.user)
        response = self.client.get('/reports/')
        response_data = response.json()
        
        # Debugging: Print response details
        print('Status Code:', response.status_code)
        print('Response Data:', response_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Report', [item['title'] for item in response_data])