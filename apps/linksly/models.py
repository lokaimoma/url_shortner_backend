from django.contrib.auth.models import User
from django.db import models


class URL(models.Model):
    status_choices = [
        ('ACTIVE', 'ACTIVE'),
        ('OFFLINE', 'OFFLINE')
    ]
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, primary_key=True)
    long_url = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200, default='ACTIVE', choices=status_choices)


class Redirect(models.Model):
    url = models.ForeignKey(to=URL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    count = models.IntegerField()
