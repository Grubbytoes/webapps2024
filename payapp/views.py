from django.contrib.auth import login as auth_login
from django.db import transaction
from django.http import HttpResponseBadRequest
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

    return render(request, 'forms/base_form.html', {
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
    return render(request, 'forms/make_a_payment.html', context)


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
    return render(request, 'forms/request_a_payment.html', context)


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
    return render(request, 'user_info/my_account.html', context)


def my_notifications(request):
    context = default_context(request, "My Notifications")

    if 'clear_notifications' in request.GET:
        request.user.clear_notifications()

    context["notification_list"] = request.user.notification_list()
    return render(request, "user_info/my_notifications.html", context)


def my_payments(request):
    context = default_context(request, "My Payments")
    payments_all = request.user.payments_all()
    payments_list = []

    # Build the payments list as a human-readable thing
    for p in payments_all:
        sent = (p.sender == request.user.holding)
        stuff: tuple
        if sent:
            # Then, this is a payment we sent
            stuff = (
                True,
                p.recipient.account.name_str(),
                p.value_str(),
                p.date_made
            )
        else:
            # This is a payment we received
            stuff = (
                False,
                p.sender.account.name_str(),
                # This is ugly
                p.value_str(format_for_recipient=True),
                p.date_made
            )
        payments_list.append(stuff)

    context["payment_list"] = payments_list
    return render(request, "user_info/my_payments.html", context)


def my_requests(request):
    context = default_context(request, "My requests")
    requests_all = request.user.requests_all()
    request_list = []

    if 'acc_req' in request.GET:
        req_id = request.GET.get('acc_req')
        req = models.Request.objects.get(pk=req_id)

        # Guard against false requests
        if req.sender != request.user.holding:
            return HttpResponseBadRequest()
        if not req.is_possible():
            context["impossible"] = True
        elif "proceed" in request.GET:
            if req.accept():
                context['done'] = True
            else:
                context['error'] = True
        else:
            context["request_details"] = (
                req.recipient.account.name_str(), req.value_str(format_for_recipient=True), req.id
            )

        return render(request, 'user_info/accept_request.html', context)

    elif 'rej_req' in request.GET:
        req_id = request.GET.get('rej_req')
        req = models.Request.objects.get(pk=req_id)
        context["request_details"] = (
            req.recipient.account.name_str(), req.value_str(format_for_recipient=True), req.id
        )

        # Guard against false requests
        if req.sender != request.user.holding:
            return HttpResponseBadRequest()
        elif "proceed" in request.GET:
            if req.reject():
                context['done'] = True
            else:
                context['error'] = False

        return render(request, 'user_info/reject_request.html', context)

    for r in requests_all:
        sent = (r.recipient == request.user.holding)
        stuff: tuple

        if sent:
            # A request we made, IE a request for a transaction where WE are the recipient
            stuff = (
                True, r.sender.account.name_str(), r.value_str(format_for_recipient=True), r.date_made, r.status
            )
        else:
            # A request made OF US
            stuff = (
                False, r.recipient.account.name_str(), r.value_str(), r.date_made, r.status, r.id
            )

        request_list.append(stuff)

    context["request_list"] = request_list
    return render(request, "user_info/my_requests.html", context)
