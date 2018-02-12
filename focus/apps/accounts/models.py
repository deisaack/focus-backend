from django.db import models
from django.contrib.auth import get_user_model
import os
from django.conf import settings
from focus.utilities import common

User=get_user_model()


def id_location(instance, filename):
    path = str(instance.user.username) + '/'
    # filename = 'national_id.png'
    return os.path.join(path, filename)


def image_location(instance, filename):
    path = str(instance.user.username) + '/images/'
    filename = 'national_id.png'
    return os.path.join(path, filename)


class Employee(models.Model):
    MALE='M'
    FEMALE='F'
    NA='N/A'
    GENDER_CHOICES=(
        ('male', MALE),
        ('female', FEMALE),
        ('N/A', NA)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_no = models.CharField(null=True, blank=True, max_length=100)
    date_hired = models.DateField(null=True, blank=True)
    id_no = models.PositiveIntegerField(null=True, blank=True, unique=True)
    id_file = models.FileField(upload_to=id_location, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    gender=models.CharField(max_length=3, default=NA)
    image=models.ImageField(upload_to=image_location, null=True, blank=True)
    phone_verified=models.BooleanField(default=False)
    tax_pin = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return "{}'s profile". format(self.user.username)

    @property
    def get_picture(self):
        if self.image:
            url = self.image.url
        elif self.gender == self.MALE:
            url = settings.STATIC_URL + 'img/default/male.png'
        elif self.gender == self.FEMALE:
            url = settings.STATIC_URL + 'img/default/female.png'
        else:
            url = settings.STATIC_URL + 'img/default/user.png'
        return url

