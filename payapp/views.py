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

    # if logged_in:
    #     pass
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
        context = default_context(request, "log out")
        return render(request, 'logout.html', context)


def make_payment(request):
    # Variables
    errors = []
    context = default_context(request, "make payment")
    context.update({
        'form': forms.MakePayment(),
        'errors': errors
    })

    # Functions
    def try_make_payment(form_: forms.MakePayment) -> bool:
        if not form_.is_valid():
            return False

        # Get data out of the form
        form_data = form_.cleaned_data
        sender = request.user.holding
        amount: int

        # Make sure the amount if valid
        try:
            amount = int(form_data['value'])
        except ValueError:
            errors.append("\"{}\" is not a valid amount of money".format(form_data['value']))
            return False

        # Make sure they can afford it
        if sender.balance < amount:
            errors.append("Your balance is not enough for this transaction")

        # Search for the recipient
        query = models.UserAccount.objects.filter(username=form_data['recipient'])
        if not query.exists():
            errors.append('User "{0}" could not be found'.format(form_data['recipient']))
            return False
        recipient: models.Holding = query[0].holding

        # NOW we have our recipient, we are ready to make a transaction:
        with transaction.atomic():
            sender.balance -= amount
            recipient.balance += amount

            sender.save()
            recipient.save()

            # Finally, log the transaction
            t = models.Transaction(value=amount)
            t.sender = sender
            t.recipient = recipient
            t.save()
            return True

    # POST
    if request.method == 'POST':
        form_in = forms.MakePayment(request.POST)
        success = try_make_payment(form_in)

        if success:
            context['success'] = "Payment made! make another?"

    # Template
    return render(request, 'default_form.html', context)


def request_payment(request):
    # Variables
    logged_in = request.user.is_authenticated
    errors = []
    context = default_context(request, "request payment")
    context.update({
        'form': forms.RequestPayment(),
        'errors': errors
    })

    # POST
    if request.method == 'POST':
        pass

    # Template
    return render(request, 'default_form.html', context)


def my_account(request):
    context = default_context(request, 'my account')
    context.update(
        {
            "balance": request.user.balance_str(),
            "payments_made": request.user.get_payments_made(),
            "payments_received": request.user.get_payments_received()
        }
    )

    return  render(request, 'my_account.html', context)