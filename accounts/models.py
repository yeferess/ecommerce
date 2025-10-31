from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return self.user.username