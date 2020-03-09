from django import forms

class Registration(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(max_length=32, widget=forms.PasswordInput)
  password_verify = forms.CharField(max_length=32, widget=forms.PasswordInput)

class Login(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(max_length=32, widget=forms.PasswordInput)