# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Attendance(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Association with UserProfile
    date = models.DateField(default=timezone.now)  # Attendance date
    time = models.TimeField(default=timezone.now)  # Attendance time
    status = models.CharField(max_length=10, default="Present")  # Attendance status

    def __str__(self):
        return f'Attendance for {self.user_profile.name} on {self.date}'
