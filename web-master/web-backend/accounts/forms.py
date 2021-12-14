from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class LoginForm(forms.Form):
    uos_id = forms.CharField(
        label='ID',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'UOS_portal_ID',
                'required': 'True',
            }
        ),
        max_length=30,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
                'required': 'True',
            }
        ),
    )
    fields = ['uos_id', 'password']

#-- 사용자 생성 폼
class UserCreationForm(forms.ModelForm):
    uos_id = forms.CharField(
        label='UOS portal ID',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'UOS portal ID',
                'required': 'True',
            }
        ),
        max_length=30,
    )
    name = forms.CharField(
        label='name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'name',
                'required': 'True',
            }
        ),
        max_length=20,
    )
    student_id = forms.CharField(
        label='UOS student ID',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'student ID',
                'required': 'True',
            }
        ),
        max_length=10,
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
    )
    password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password confirmation',
            }
        ),
    )
    
    class Meta:
        model = User
        fields = ('uos_id', 'name', 'student_id')

    def clean_password2(self):
        # 비밀번호 일치 확인
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

#-- 비밀번호 변경 폼
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label = 'password'
    )

    class Meta:
        model = User
        fields = ('uos_id', 'name', 'student_id', 'password')

    def clean_password(self):
        return self.initial['password']