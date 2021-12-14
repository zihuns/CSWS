"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from project import views as project_views
from shell import views as shell_views
from web_hosting import views as web_hosting_views
from accounts import views as accounts_views
from webcompiler import views as webcompiler_views
from homeworkpost_compile_grade.views import create_post2

from django.views.static import serve 
from django.conf import settings



urlpatterns = [
    # static ?åå?ùº
    re_path('static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT }),
    
    # Í¥?Î¶¨Ïûê ?ôîÎ©?
    path('admin/', admin.site.urls),

    # ?ôà ?ôîÎ©?
    path('', project_views.Home.as_view(), name='home'),

    # accounts
    path('login/', accounts_views.LoginView.as_view(), name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('signup/', accounts_views.SignupView.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>/', accounts_views.activate, name='activate'),
    path('mypage/', accounts_views.MyPageView.as_view(), name='mypage'),

    # shell
    path('shell/', shell_views.shell_view, name='shell'),
    path('shell/create_container', shell_views.create_container, name='create_container'),
    path('shell/delete_container', shell_views.delete_container, name='delete_container'),

    # web_hosting
    path('web_hosting/', include('web_hosting.urls')),
    path('web_hosting/delete/', web_hosting_views.delete_file, name='delete_file'),


    #homeworkpost_compile_grade
    path('homeworkpost_compile_grade/', create_post2, name = "create2"),

    # Í≤åÏãú?åê
    path('boards/', include('boards.urls')),
]
