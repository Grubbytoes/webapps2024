from django.contrib.auth import login as auth_login
from django.db import transaction
from django.shortcuts import render, redirect

from webapps2024.views import default_context
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
        if len(query) == 0:
            return False

        # Check password
        user_by_name: models.UserAccount = query[0]
        if not user_by_name.check_password(data['password']):
            return False

        auth_login(request, user_by_name)
        return True

    if request.method == "POST":
        logged_in = try_login(forms.LoginForm(request.POST))
        if not logged_in:
            errors.append('Incorrect username or password')
        else:
            return redirect('/home')

    return render(request, 'base_form.html', {
        'page_title': 'login',
        'form': forms.LoginForm(),
        'errors': errors,
        'logged_in': False
    })


def logout(request):
    if not request.user.is_authenticated:
        return redirect('/home')
    else:
        context = default_context(request, "log out")
        return render(request, 'logout.html', context)


def make_payment(request):
    # Variables
    errors = []
    context = default_context(request, "make payment")
    context.update({
        'form': forms.MakePayment(),
        'errors': errors,
    })

    # Functions
    def try_make_payment(form_: forms.MakePayment) -> bool:
        if not form_.is_valid():
            errors.append("There was a problem: the form sent is invalid")
            return False
        form_data = form_.cleaned_data
        sender: models.Holding = request.user.holding
        recipient_user = models.UserAccount.user_by_name(form_data['recipient'])
        amount_to_pay = form_data['value']

        # Make sure the amount if valid
        if sender.balance < amount_to_pay:
            errors.append("Sorry, you do not have enough money to make this payment")
            return False
        elif recipient_user is None:
            errors.append("That user could not be found, are you sure you got their name right?")
            return False
        elif recipient_user == request.user:
            errors.append("You cannot send money to yourself")
            return False
        recipient_holding = recipient_user.holding

        # MAKE IT SO
        if not sender.send_payment(recipient=recipient_holding, amount=amount_to_pay):
            errors.append("Something went wrong, no money has left your account")
        else:
            return True

    # POST
    if request.method == 'POST':
        form_in = forms.MakePayment(request.POST)
        if try_make_payment(form_in):
            context['success'] = "Payment made! make another?"

    # GET or payment unsuccessful
    # Template
    return render(request, 'make_a_payment.html', context)


def request_payment(request):
    # Variables
    logged_in = request.user.is_authenticated
    errors = []
    context = default_context(request, "request payment")
    context.update({
        'form': forms.RequestPayment(),
        'errors': errors
    })

    def try_make_request(form_: forms.RequestPayment):
        if not form_.is_valid():
            errors.append("There was a problem: the form sent is invalid")
            return False

        form_data = form_.cleaned_data
        requested_from_account = models.UserAccount.user_by_name(form_data['sender'])
        requested_by = request.user.holding

        if requested_from_account is None:
            errors.append("No such user exists, are you sure you got their name right?")
            return False
        elif requested_from_account == request.user:
            errors.append("You cannot request money from yourself.")
            return False
        requested_from = requested_from_account.holding

        requested_by.send_request(requested_from, form_data['value'])
        return True

    # POST
    if request.method == 'POST':
        if try_make_request(forms.RequestPayment(request.POST)):
            context['success'] = "A request has been sent!"

    # Template
    return render(request, 'request_a_payment.html', context)


def my_account(request):
    context = default_context(request, 'my account')
    account_data = {
        "balance": request.user.balance_str(),
        "payments_made": request.user.payments_made_count(),
        "payments_received": request.user.payments_received_count(),
        "requests_sent": request.user.requests_sent_count(),
        "requests_received": request.user.requests_received_count()
    }
    context["account_data"] = account_data
    return render(request, 'my_account.html', context)


def my_notifications(request):
    context = default_context(request, "My Notifications")

    if 'clear_notifications' in request.GET:
        request.user.clear_notifications()

    context["notification_list"] = request.user.get_notifications()
    return render(request, "my_notifications.html", context)
