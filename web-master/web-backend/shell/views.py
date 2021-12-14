from django.shortcuts import render, redirect
from .models import Container
from django.urls import reverse_lazy
from project import views as project_views
from subprocess import Popen
import os

def shell_view(request):
    containers = Container.objects.get(user=request.user)
    

    if containers.ipaddr != "":
        split_ipaddress = containers.ipaddr.split('.')

        context = {
            'is_created': containers.flag,
            'container_ip': containers.ipaddr,
            'container_port': int(split_ipaddress[3])+20000,
        }

    else:
         context = {
            'is_created': containers.flag,
            'container_ip': containers.ipaddr,
            'container_port': '',
        }
        
    return render(request, 'shell.html', context)
    
def create_container(request):
    
    containers = Container.objects.get(user=request.user)

    containers.flag = True
    os_name = request.POST.get('os')
    containers.osname = os_name

    containers.save()

    username = request.user.uos_id
    
    print(os_name)
    print(username)

    Popen(["/root/openstack/scripts/make_instance.sh" , username ,os_name ])
 #   os.system("/root/openstack/scripts/make_instance.sh" + " " + username + " " + os_name)

    return redirect('home') 

def delete_container(request):

    containers = Container.objects.get(user=request.user)

    if containers.flag == True:
        containers.flag = False
        containers.ipaddr = ""

        os_name = containers.osname
        username = request.user.uos_id

        containers.osname =""

        print(os_name)
        print(username)

        containers.save()
#       Popen(["/root/openstack/scripts/delete_container_with_user_id_and_user_os.sh" , username ,os_name ])
        os.system("/root/openstack/scripts/delete_container_with_user_id_and_user_os.sh" + " " + username + " " + os_name)

        return redirect('/shell')

    else:
        return redirect('/shell')

