from django import forms
from payapp import models


class RegisterForm(forms.Form):
    username = forms.CharField(label="Your Username")
    email = forms.EmailField(label="Your Email")
    email_conf = forms.EmailField(label="Your Email")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)
    password_conf = forms.CharField(label="Your Password", widget=forms.PasswordInput)

    def is_valid(self):
        if super(self).is_valid():
            if self.data['email'] != self.data['email_conf']:
                return False
            if self.data['password'] != self.data['password_conf']:
                return False
            return True
        return False


class SetUp(forms.Form):
    first_name = forms.CharField(label="Your First Name")
    last_name = forms.CharField(label="Your Last Name")
    currency = forms.ChoiceField(label="Your native currency", choices=models.CURRENCIES)
    _piggy_back = {"set": False}

    def set_piggy_back(self, username, email, password):
        self._piggy_back.update({"set": True, "username": username, "email": email, "password": password})

    def get_piggy_back(self):
        return {
            "password": self._piggy_back["password"],
            "username": self._piggy_back["username"],
            "email": self._piggy_back["email"]
        }
