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
    status = models.CharField(max_length=200, default=status_choices[0][0], choices=status_choices)
    redirects = models.IntegerField(default=0, blank=True)
