from dataclasses import fields
from django import forms
from django.forms import ModelForm
from App_account.models import User,Profile,ProfilePic
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password1','password2')
        # this field is User field whice are required field form User abstractbased model please remind it

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ('images',)