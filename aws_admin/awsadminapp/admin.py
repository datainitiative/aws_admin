from django.contrib import admin

from awsadminapp.models import *

class MyUserAdmin(admin.ModelAdmin):
    fields = ['user','is_online','last_start_instance']
    list_display = ('user','_get_user_first_name','_get_user_last_name','is_online','last_start_instance')
    search_fields = ['user','_get_user_first_name','_get_user_last_name','is_online','last_start_instance']
admin.site.register(MyUser,MyUserAdmin)
