
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(default=timezone.now)
    governorate = models.CharField(max_length=255, null=True, blank=True)
    markaz = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

# Token model for storing authentication tokens
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


# Issue model
class Issue(models.Model):
    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('emergency', 'Emergency'),
    ]

    STATUS_CHOICES = [
        ('face_1', 'Reported'),
        ('face_2', 'Reported and seen'),
        ('face_3', 'Reported and seen and solved'),
    ]

    CAT = [
        ('issue', 'Issue'),
        ('emergency', 'Emergency'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='issue_photos/')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    category = models.CharField(max_length=10, choices=CAT, default='open')
    def __str__(self):
        return self.title

class Review:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    difficulty = models.BooleanField()
    is_solved = models.BooleanField()
    def __str__(self):
        return f"Review from {self.user.firstname} with the comment: {self.comment}"

# Optional Admin-specific model if needed
class Dashboard(models.Model):
    data = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin Dashboard for {self.admin.username}"
    
class AI(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE)
    ai_description = models.TextField(null=True, blank=True)
    ai_solution = models.TextField(null=True, blank=True)
    ai_danger_level = models.CharField(max_length=10, choices=Issue.LEVEL_CHOICES, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=Issue.LEVEL_CHOICES, null=True, blank=True)
    concerned_authority_name = models.TextField(null=True, blank=True)
    nearest_branch = models.TextField(null=True, blank=True)
    report_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    def __str__(self):
        return f"AI Analysis for Issue: {self.issue.title}"
    




