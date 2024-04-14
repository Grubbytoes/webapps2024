from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Your Username")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)


class MakePayment(forms.Form):
    payment_to = forms.CharField(label="Recipient Username")
    value = forms.IntegerField(label="Amount", widget=forms.TextInput)


class RequestPayment(MakePayment):
    pass
