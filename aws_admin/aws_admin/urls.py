from django.conf.urls import patterns, include, url
from django.contrib import admin
from aws_admin.settings import ROOT_APP_URL

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aws_admin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    # AWS Admin App URLs
    url(r'^%s/' %  ROOT_APP_URL.replace("/aws_admin/",""),include('awsadminapp.urls')),     
)
