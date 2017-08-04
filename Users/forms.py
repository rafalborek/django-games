from django.contrib.auth.models import User
from django import forms

class UserFormRegister(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email','password']
        
        
class UserFormLogin(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    
    class Meta:
        model = User
        fields = ['username','password']
        
        
class UserFormUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email']