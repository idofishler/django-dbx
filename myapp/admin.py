from django.contrib import admin
from myapp.models import DbxUser

class DbxUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'dbx_user_id', 'dbx_access_token')
    search_fields = ['username']

admin.site.register(DbxUser, DbxUserAdmin)
