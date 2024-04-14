from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from . import forms, models

# Global functions

# Create your views here.

def login(request):
    # Variables
    logged_in = False
    errors = []

    # Methods
    def try_login(form_) -> bool:
        if not form_.is_valid():
            return False
        data = form_.cleaned_data

        # Try and find a user of the right name
        query = models.UserAccount.objects.filter(username=data['username'])
        if query is None:
            return False

        # Check password
        user_by_name: models.UserAccount = query[0]
        if not user_by_name.check_password(data['password']):
            return False

        auth_login(request, user_by_name)
        return True

    if request.method == "POST":
        logged_in = try_login(forms.LoginForm(request.POST))
        if not logged_in: errors.append('Incorrect username or password')
        else: return redirect('/home')

    if logged_in:
        pass
    else:
        return render(request, 'default_form.html', {
            'page_title': 'login',
            'form': forms.LoginForm(),
            'errors': errors,
            'logged_in': False
        })


def logout(request):
    if not request.user.is_authenticated:
        return redirect('/home')
    else:
        context = {'page_title': 'logout from payapp', 'logged_in': True}
        return render(request, 'logout.html', context)


def make_payment(request):
    # Variables
    logged_in = request.user.is_authenticated
    errors = []
    context = {
        'page_title': 'Make a payment',
        'form': forms.MakePayment(),
        'errors': errors,
        'logged_in': logged_in
    }

    # Template
    return render(request, 'default_form.html', context)


def request_payment(request):
    # Variables
    logged_in = request.user.is_authenticated
    errors = []
    context = {
        'page_title': 'Request a payment',
        'form': forms.RequestPayment(),
        'errors': errors,
        'logged_in': logged_in
    }

    # Template
    return render(request, 'default_form.html', context)
