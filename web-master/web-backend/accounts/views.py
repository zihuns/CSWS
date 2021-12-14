from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.views.generic.base import View, TemplateView
from django.contrib.auth import login, logout, authenticate

from .forms import LoginForm, UserCreationForm
from .models import User
from .tokens import account_activation_token

from shell.models import Container



#--- Login View
class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    

    # 빈 로그인 창 띄우기 
    def get(self, request):
        # 이미 로그인 한 사용자
        if request.user.is_authenticated:
            return redirect('home')

    # 로그인
    def post(self, request):
        # 이미 로그인 한 사용자
        if request.user.is_authenticated:
            return redirect('home')

        form = self.form_class(request.POST)
        
        if form.is_valid():
            uos_id = form.cleaned_data['uos_id']
            password = form.cleaned_data['password']
            user = authenticate(uos_id=uos_id, password=password)
            # 로그인 성공
            if user is not None:
                login(request, user)
                return redirect('home')

        # 로그인 실패
        return render(request, self.template_name, {'form': form})
        


#--- Logout
def logout_view(request):
    # 로그인 한 사용자
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')


#--- Signup View
class SignupView(View):
    form_class = UserCreationForm
    template_name = "accounts/signup.html"

    def get(self, request):
        # 이미 로그인 한 사용자
        if request.user.is_authenticated:
            return redirect('home')

    # 회원가입
    def post(self, request):
        # 이미 로그인 한 사용자
        if request.user.is_authenticated:
            return redirect('home')

        form = self.form_class(request.POST)
        # 유효한 값이 들어옴
        if form.is_valid():
            # 비밀번호와 비밀번호 체크가 같음
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                uos_id = form.cleaned_data['uos_id']
                name = form.cleaned_data['name']
                student_id = form.cleaned_data['student_id']
                password = form.cleaned_data['password']
                new_user = User.objects.create_user(uos_id=uos_id, name=name, student_id=student_id, password=password)
                new_user.is_active = False
                new_user.save()
                current_site = get_current_site(request)
                mail_title = "계정 활성화 확인 이메일"
                message = render_to_string('activation_email.html', {
                    'user': name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                })
                new_user.email_user(mail_title, '', html_message=message)
                

                return redirect('home')
                
            # 비밀번호와 비밀번호체크가 다를 경우
            else: 
                return render(request, self.template_name, {'form': form, 'error': '비밀번호가 다릅니다.'})
        # 유효한 값이 아님
        else:
            return render(request, self.template_name, {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        container = Container.objects.create(user=user,ipaddr="",username=user.uos_id)

        return redirect('home')

    else:
        return render(request, 'home.html', {'error': '계정 활성화 오류'})

#-- MyPageView
class MyPageView(View):
    template_name = 'accounts/mypage.html'

    def get(self, request):
        # 인증되지 않은 사용자
        if not request.user.is_authenticated:
            return redirect('login')
        
        return render(request, self.template_name)
