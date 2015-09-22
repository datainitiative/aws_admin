from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import datetime

class MyUser(models.Model):
#    id =  models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    is_online = models.BooleanField(default=False)
    last_start_instance = models.DateTimeField(auto_now=False,auto_now_add=False,null=True,blank=True)
    
    def __unicode__(self):
        return "%s %s" % (self.user.first_name,self.user.last_name)
    
    def _get_user_first_name(self):
        if self.user.first_name:
            return self.user.first_name
        else:
            return ""
    _get_user_first_name.short_description = "First Name"
        
    def _get_user_last_name(self):
        if self.user.last_name:
            return self.user.last_name
        else:
            return ""
    _get_user_last_name.short_description = "Last Name"
    
    def _get_user_email(self):
        if self.user.email:
            return self.user.email
        else:
            return ""
    _get_user_email.short_description = "Email Address"
    
    class Meta:
        db_table = u'app_user'
