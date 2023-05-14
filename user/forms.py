from django import forms
from user.models import User


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='')


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirmpassword']
        labels = {'name':'', 'email':'', 'password':'','confirmpassword':''}
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'confirmpassword': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
        }
