from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  # this AbstractUser extends the default Django User model
    profile_pic = models.ImageField(upload_to="profile_image/", default="profile_image/default.jpg", blank=True, null=True)
    bio = models.TextField(max_length=250, blank=True)
