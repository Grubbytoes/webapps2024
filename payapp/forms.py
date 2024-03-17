from django import forms


class LoginForm(forms.Form):
    """
    Simple form for logging in
    """
    username = forms.CharField(label="Your Username")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)
