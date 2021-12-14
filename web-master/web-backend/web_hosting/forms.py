# -*- coding: utf-8 -*-
from django import forms
from .models import File
#'webkitdirectory': True, 'directory':True
class FileForm(forms.ModelForm):
       file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory':True} ))
    #    sid = forms.CharField(max_length=10)

       class Meta:
           model = File
           fields = ['file']
        #    fields = ['file', 'sid']