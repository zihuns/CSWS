# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FileForm
from .models import File
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from datetime import datetime
import pytz # $ pip install pytz

#from __future__ import unicode_literals

from django.views import View

from .models import *
from accounts.models import User
from django.forms import modelformset_factory


def upload_file(request):
        files = File.objects.filter(sid=request.user)
        # files = File.objects.all()
        files.날짜 = datetime.now(pytz.timezone('Asia/Seoul')).utcoffset()
        total_size = sum([ x.file.size for x in File.objects.all().filter(sid=request.user) ])
        # user = get_object_or_404(User, uos_id=request.user.uos_id)
        max_size = 1073741824
        if request.method == 'GET':
           form = FileForm(None)
        elif request.method == 'POST':

            if total_size > max_size:
                messages.success(request,'Please keep filesize under 1gb')
                return redirect('upload_file')
            else :
                #for index, _file in enumerate(request.FILES.getlist('file')):
                for _file in request.FILES.getlist('file'):
                    request.FILES['file'] = _file
                    form = FileForm(request.POST, request.FILES)
                    if form.is_valid():
                        total_size = sum([ x.file.size for x in File.objects.all().filter(sid=request.user) ])
                        #_new = File.objects.get(id=_file[index].id)
                        
                        _new = form.save(commit=False)
                        check_size = total_size + _new.file.size
                        if check_size > max_size:
                            return redirect('upload_file')
                            
                        _new.sid = request.user
                        _new.save()
                        form.save_m2m()
                
        total_size = sum([ x.file.size for x in File.objects.all().filter(sid=request.user) ])
        percent = round(total_size/max_size,2)*100
        context = {'form': form, 'files': files, 'total_size': total_size, 'max_size': max_size, 'request.user': request.user, 'percent': percent,}
        return render(request, 'web_hosting/upload_file.html', context)



def delete_file(request):
    
    pks = request.POST.getlist('pk')
    
    for pk in pks:
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('upload_file')


#def delete_file(request, pk):
 #   if request.method == 'POST':
  #      file = File.objects.get(pk=pk)
  #      file.delete()
   # return redirect('upload_file')



def file_list(request):
    files = File.objects.all()
    return render(request, 'web_hosting/upload_file.html', {
        'files' : files
    })
