from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import logout

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('awsadminapp.views',
	# Home page URL
	url(r'^home/$','home'),
	
	# Login,Logout,Register,User
	url(r'^logout/$',logout,{'template_name': 'registration/logged_out.html'}),
	url(r'^user/profile/$','user_profile'),
	url(r'^user/password/$','user_change_password'),
	
	# Start, Stop Server
	url(r'^startserver/(?P<instance_id>.*)/$','start_server'),
	url(r'^stopserver/(?P<instance_id>.*)/$','stop_server'),
)