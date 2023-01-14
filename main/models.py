from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


def question_file_name(instance, filename):
    return '/'.join([f'questions/', filename])

class Group(AbstractUser):
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



class Question(models.Model):
    answer = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    sort_number = models.IntegerField()
    img = models.ImageField(upload_to=question_file_name, null=True, blank=True)
    is_question = models.BooleanField(default=False)


class Answer(models.Model):
    text = models.CharField(max_length=10)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)