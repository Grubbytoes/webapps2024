from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(label="Your Username")
    email = forms.EmailField(label="Your Email")
    first_name = forms.CharField(label="Your First Name")
    last_name = forms.CharField(label="Your Last Name")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)