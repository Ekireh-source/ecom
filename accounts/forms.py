from django import forms
from .models import User



class UserLogin(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'email',
        'placeholder' : 'Enter Email',
        'type' : 'email'
    }))
    password = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'password',
        'placeholder' : 'Enter Password',
        'type' : 'password'
    }))


class UserRegister(forms.Form):
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'first_name',
        'placeholder' : 'Enter First Name',
        'type' : 'text'
    }))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'last_name',
        'placeholder' : 'Enter Last Name',
        'type' : 'text'
    }))
    email = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'email',
        'placeholder' : 'Enter Email',
        'type' : 'email'
    }))
    password = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'password',
        'placeholder' : 'Enter Password',
        'type' : 'password'
    }))
    confirm_password = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'name' : 'confirm_password',
        'placeholder' : 'Confirm Your Password',
        'type' : 'password'
    }))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password', 'is_admin', 'is_staff')