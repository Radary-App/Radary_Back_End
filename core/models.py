
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
import os

# Custom User model
class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)

    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    governorate = models.CharField(max_length=255, null=True, blank=True)
    markaz = models.CharField(max_length=255, null=True, blank=True)

    username = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username}"

# Token model for storing authentication tokens
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

# Report model
class Problem(models.Model):
    STATUS_CHOICES = [
        ('face_1', 'Reported'),
        ('face_2', 'Reported and seen'),
        ('face_3', 'Reported and seen and solved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='face_1')

    coordinates = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='problem_photos/', blank=True, null=True) ## change to required in production
    user_description = models.CharField(max_length=255, null=True, blank=True)
    
    conclusion = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Report by {self.user.username} on {self.created_at} with status {self.status}"
    def delete(self, *args, **kwargs):
        # Delete the photo from the file system
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)

class Emergency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='emergency_photos/')
    coordinates = models.CharField(max_length=255)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def delete(self, *args, **kwargs):
       
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Emergency by {self.user.username} on {self.created_at}"

class Review(models.Model):
    related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    related_report = models.ForeignKey(Problem, related_name='review', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=True, blank=True)
    difficulty = models.BooleanField(null=True, blank=True)
    is_solved = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.related_user.first_name} with username: {self.related_user.username}\n for report: {self.related_report}\n with comment: {self.comment}"


class Authority(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)


    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Authority: {self.name} with email: {self.email}"

class Authority_Locations(models.Model):
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    governorate = models.CharField(max_length=255)
    markaz = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Authority: {self.authority.name} in {self.governorate}, {self.markaz}"
    

# Optional Admin-specific model if needed


class AI_Problem(models.Model):
    report = models.OneToOneField(Problem, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    priority = models.IntegerField(null=True, default=0) # 1 - 5 --> 1 is the highest
    authority_name = models.ForeignKey(Authority, related_name='ai_problems', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    subdivision = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"AI_Problem Analysis for Report_ID: {self.report.id} by {self.report.user.username}"

class AI_Emergency(models.Model):
    report = models.OneToOneField(Emergency, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    danger_level = models.IntegerField(null=True, default=0) # 1 - 100 --> 100 is the highest
    authority_name = models.ForeignKey(Authority, related_name='ai_emergencies', on_delete=models.CASCADE)

    def __str__(self):
        return f"AI_Emergency Analysis for Report_ID: {self.report.id} by {self.report.user.username}"


class Summary(models.Model):
    summary = models.CharField(max_length=1500)
    review_ids = models.CharField(max_length=255)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Summary for reports: {self.review_ids}"