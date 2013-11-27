from django.db import models
from django.contrib import auth

class DbxUser(auth.models.User):
    class Meta:
        verbose_name = 'Dropbox User'
        verbose_name_plural = 'Dropbox Users'

    user = models.OneToOneField(auth.models.User)
    dbx_user_id = models.CharField(max_length=200, blank=True, null=True)
    dbx_access_token = models.CharField(max_length=200, blank=True, null=True)
