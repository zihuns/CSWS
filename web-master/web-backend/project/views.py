from django.views.generic.base import View
from django.shortcuts import render, redirect

#--- 홈 화면
class Home(View):
    template_name = 'home.html'
    
    def get(self, request):
        return render(request, self.template_name)
