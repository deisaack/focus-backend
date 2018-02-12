from django.db import models
from django.contrib.auth import get_user_model
from focus.utilities import common
User=get_user_model()


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(common.get_sentinel_user), related_name='files')
    detail = models.CharField(max_length=500, default='')
    item = models.FileField(upload_to='files')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # approvers = models.ManyToManyField(User, related_name='verifiers', blank=True, through='Approval')

    def __str__(self):
        return self.detail


class Approval(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(common.get_sentinel_user))
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.file.detail
