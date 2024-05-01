from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Your Username")
    password = forms.CharField(label="Your Password", widget=forms.PasswordInput)


class MakePayment(forms.Form):
    recipient = forms.CharField(label="Recipient Username")
    value = forms.FloatField(label="Amount", widget=forms.TextInput, min_value=0, step_size=0.01)


class RequestPayment(forms.Form):
    sender = forms.CharField(label="Sender Username")
    value = forms.FloatField(label="Amount", widget=forms.TextInput, min_value=0, step_size=0.01)

