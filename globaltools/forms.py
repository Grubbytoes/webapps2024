from django import forms
from . import models as mymodels


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    email = forms.CharField(label="Email", max_length=100)
    email_c = forms.CharField(label="Confirm Email", max_length=100)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)
    password_c = forms.CharField(label="Confirm Password", max_length=50, widget=forms.PasswordInput)

    def is_valid(self):
        v: bool = forms.Form.is_valid(self)
        # Email matches confirmation
        if self.data['email'] == self.data['email_c']:
            v = False
            self.add_error('email', 'email and email confirmation fields do not match')
        # Password matches confirmation
        if self.data['password'] == self.data['password_c']:
            v = False
            self.add_error('password', 'password and password confirmation fields do not match')
        return v


class LoginForm(forms.Form):
    """
    Simple form for logging in
    """
    username = forms.CharField(label="Your Username")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)

    def authenticate_user(self) -> int:
        """
        Searches for a user with the given details, and checks their password
        returns user id if successful
        :return:
        """
        input_username = self.data['username']
        input_password = self.data['password']
        found_user = mymodels.UserAccount.objects.all().filter(username=input_username)

        # Check that any such user exists
        if not found_user:
            return -1

        # Check password
        user: mymodels.UserAccount = found_user[0]
        id_code = user.authenticate_password(input_password)

        return id_code
