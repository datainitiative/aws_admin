from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext
from django.db import models
from django.db.models.loading import get_model
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone

# Import from Python
import boto3
from boto3.session import Session as Boto3Session
import time,json

# Import from general utilities
from util import *

# Import from app
from aws_admin.settings import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, INSTNACE_ID_WINDOWS, ROOT_APP_URL
from awsadminapp.forms import *
from awsadminapp.models import *

'''-----------------------
User functions
-----------------------'''   
# User Profile
@login_required
@render_to("awsadminapp/user_profile.html")
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        user_profile_form = UserProfileForm(instance=user)
    elif request.method == 'POST':
        user_profile_form = UserProfileForm(data=request.POST, instance=user)
        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.info(request, "User profile was changed successfully.")
            if 'save' in request.POST:
                if "next" in request.GET:
                    #app_name = request.GET["next"].replace(APP_SERVER_URL,"").partition("/")[2].partition("/")[0]
                    return HttpResponseRedirect(request.GET["next"])
                else:
                    return HttpResponseRedirect('%s/home/' % ROOT_APP_URL)                
        else:
            messages.error(request, "Please correct the errors below.")
    return {'user_name':user.username,'user_profile_form':user_profile_form}

# User Change Password
@login_required
@render_to("awsadminapp/user_password.html")
def user_change_password(request):
    user = request.user
    if request.method == 'GET':
        user_password_form = PasswordChangeForm(user)
    elif request.method == 'POST':
        user_password_form = PasswordChangeForm(user,request.POST)
        if user_password_form.is_valid():
            user_password_form.save()
            messages.info(request, "User password was changed successfully.")
            return HttpResponseRedirect('%s/user/profile/' % ROOT_APP_URL)
        else:
            messages.error(request, "Please correct the errors below.")
    return {'user_name':user.username,'user_password_form':user_password_form}

'''-----------------------
Main functions
-----------------------''' 
# Get All Logged in (autenticated) Users
def get_all_logged_in_users():
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []
    
    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    
    # Query all logged in users based on id list
    return MyUser.objects.filter(user__id__in=uid_list)    


# Home page
@login_required
@render_to("awsadminapp/home.html")
def home(request):
    aws_session = Boto3Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)
    ec2 = aws_session.resource('ec2',region_name=AWS_REGION)
    
    aws_instances = ec2.instances.all()
    aws_running_instances = ec2.instances.filter(
        Filters=[{"Name":"instance-state-name","Values":["running"]}]
    )
    
    all_instance = []
    
    for instance in aws_instances:
        all_instance.append({
            "id":instance.id,
            "name":instance.tags[0]["Value"] if instance.tags else "",
            "type":instance.instance_type,
            "launch_time":instance.launch_time,
            "status":instance.state["Name"]})
    
    running_instances = []
    for instance in aws_running_instances:
        running_instances.append(instance)
        
    win_instance = ec2.Instance(INSTNACE_ID_WINDOWS)

    online_users = get_all_logged_in_users()
    for user in online_users:
        user.is_online = True
        user.save()
        
    num_user = len(online_users)
    
    all_users = MyUser.objects.all().order_by("is_online","user__first_name")
    for user in all_users:
        if user in online_users:
            user.is_online = True
        else:
            user.is_online = False
    
    return {
        "num_user":num_user,
        "num_instance":len(running_instances),
        "users":all_users,
        "instances":all_instance,
        "win_id":INSTNACE_ID_WINDOWS,
    }
    
# Start server
def start_server(request,instance_id):
    num_instance = 0
    instance_status = ""    
    if request.method == 'POST':
#        csrftoken = request.POST["csrfmiddlewaretoken"]
        if instance_id:
            aws_session = Boto3Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=AWS_REGION)
            ec2 = aws_session.resource('ec2',region_name=AWS_REGION)
            
            instance = ec2.Instance(instance_id)
            instance.start()
            
            client = ec2.meta.client
            waiter = client.get_waiter("system_status_ok")
            waiter.wait(
                DryRun = False,
                InstanceIds = [instance_id],                
            )
            waiter = client.get_waiter("instance_status_ok")
            waiter.wait(
                DryRun = False,
                InstanceIds = [instance_id],
            )

            instance_status = instance.state["Name"]            
            instance_launchtime = instance.launch_time.strftime("%b. %d, %Y %I:%M %p")
            
            aws_running_instances = ec2.instances.filter(
                Filters=[{"Name":"instance-state-name","Values":["running"]}]
            )
            running_instances = []
            for instance in aws_running_instances:
                running_instances.append(instance)
            num_instance = len(running_instances)        
            
        response_data = {
            "num_instance":num_instance,
            "instance_id":instance_id,
            "instance_status":instance_status,
            "instance_launchtime":instance_launchtime}
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    
# Stop server
def stop_server(request,instance_id):
    num_instance = 0
    instance_status = ""
    if request.method == 'POST':
#        csrftoken = request.POST["csrfmiddlewaretoken"]
        if instance_id:
            aws_session = Boto3Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=AWS_REGION)
            ec2 = aws_session.resource('ec2',region_name=AWS_REGION)
            
            instance = ec2.Instance(instance_id)
            instance.stop()
            
            instance_status = instance.state["Name"]
            
            while instance_status != "stopped":
                time.sleep(10)
                instance.reload()              
                instance_status = instance.state["Name"]
            
            aws_running_instances = ec2.instances.filter(
                Filters=[{"Name":"instance-state-name","Values":["running"]}]
            )
            running_instances = []
            for instance in aws_running_instances:
                running_instances.append(instance)
            num_instance = len(running_instances)

        response_data = {
            "num_instance":num_instance,
            "instance_id":instance_id,
            "instance_status":instance_status}
        return HttpResponse(json.dumps(response_data),content_type="application/json")    