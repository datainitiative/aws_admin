from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext
from django.db import models
from django.db.models.loading import get_model
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm

# Import from Python
import boto3
from boto3.session import Session

# Import from general utilities
from util import *

# Import from app
from aws_admin.settings import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, INSTANCE_ID_LINUX, INSTNACE_ID_WINDOWS

# Create your views here.
# Home page
#@login_required
@render_to("awsadminapp/home.html")
def home(request):
    aws_session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)
    ec2 = aws_session.resource('ec2',region_name=AWS_REGION)
    
    aws_instances = ec2.instances.all()
    aws_running_instances = ec2.instances.filter(
        Filters=[{"Name":"instance-state-name","Values":["running"]}]
    )
    for instance in aws_instances:
        print instance.id
        print instance.instance_type
    
    print "running instances:"
    running_instances = []
    for instance in aws_running_instances:
        running_instances.append(instance)
        print instance.id
        print instance.instance_type
        
    win_instance = ec2.Instance(INSTNACE_ID_WINDOWS)
    print "win instance"
    print win_instance.id
    
    return {
        "num_user":5,
        "num_instance":len(running_instances),
    }