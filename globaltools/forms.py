from django import forms


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
