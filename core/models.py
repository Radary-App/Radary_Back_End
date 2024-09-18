
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
# Custom User model
class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    governorate = models.CharField(max_length=255, null=True, blank=True)
    markaz = models.CharField(max_length=255, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User - {self.username} with email {self.email}"

# Token model for storing authentication tokens
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

# Report model
class Report(models.Model):
    STATUS_CHOICES = [
        ('face_1', 'Reported'),
        ('face_2', 'Reported and seen'),
        ('face_3', 'Reported and seen and solved'),
    ]

    CATEGORY = [
        ('issue', 'Issue'),
        ('emergency', 'Emergency'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='report_photos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='face_1')
    category = models.CharField(max_length=10, choices=CATEGORY, default='issue')
    user_description = models.CharField(max_length=255)

    coordinates = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report {self.category} by {self.user.username} on {self.created_at} with status {self.status}"

class Review:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    difficulty = models.BooleanField()
    is_solved = models.BooleanField()


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.firstname} with ID: {self.user.id} on {self.comment}"


class Authority(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    specialty = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Authority: {self.name} with the specialty: {self.specialty}"

# Police
# Fire station
# Hospital

class Authority_Locations(models.Model):
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    governorate = models.CharField(max_length=255)
    markaz = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Authority: {self.authority.name} in {self.governorate}, {self.markaz}"
    

# Optional Admin-specific model if needed
class Dashboard(models.Model):
    data = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin Dashboard for {self.admin.username}"
    
class AI(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    danger_level = models.IntegerField(null=True, default=0)
    authority_name = models.ForeignKey(Authority, related_name='authority_name', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"AI Analysis for Report: {self.report.category} by {self.report.user.username}"




