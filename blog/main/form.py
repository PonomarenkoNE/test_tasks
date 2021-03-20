from django.forms import ModelForm, EmailInput, PasswordInput, TextInput
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }


class RegForm(ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]
        widgets = {
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            "password": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            })
        }


class PostForm(forms.Form):
    header = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Header'}),
                             label='Enter name of the post')
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text'}),
                           label='Enter text')
    picture = forms.ImageField(allow_empty_file=True, required=False)


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter text'}),
                           label='Add comment')
