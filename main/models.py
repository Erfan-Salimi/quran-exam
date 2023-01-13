from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TYPE = (
        ('normal', 'Normal'),
        ('author', 'Author'),
        ('teacher', 'Teacher'),
    )

    first_name = models.CharField(max_length=20, null=True, blank=True)
    time = models.DateTimeField(default=timezone.now, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    step = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
