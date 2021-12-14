from django import forms
from .models import Post, Comment, Assignment, AssignmentSubmission
from django.contrib.admin import widgets

class PostForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'style':'margin-top:20px;'}))
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content', 'rows':'25'}))
    contain_code = forms.BooleanField(required=False, label="", widget=forms.CheckboxInput(attrs={'class': 'some_class',}))

    class Meta:
        model = Post
        fields = ('title', 'text', 'contain_code')


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder':'Comment', 'rows':'2'}))
    class Meta:
        model = Comment
        fields = ('text',)

class AssignmentForm(forms.ModelForm):
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Title', 'style':'margin-top:20px;'}))
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Content', 'rows':'25'}))
    code_submit_assignment = forms.BooleanField(required=False, label=False, help_text=" 코드 제출 과제")

    class Meta:
        model = Assignment
        fields = ('title', 'text', 'point', 'due_date', 'code_submit_assignment')

class AssignmentSubmissionForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput()
    )

    class Meta:
        model = AssignmentSubmission
        fields = ('file',)