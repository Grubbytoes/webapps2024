from django.shortcuts import render
from . import forms
from payapp import models


# Create your views here.
def register(request):
    # The variables we will use
    ok = False
    errors = []

    # Internal methods we will use
    def create_new_user(form_) -> bool:
        # Get the data from the form
        data = form_.cleaned_data

        # Check the username is OK
        if models.UserAccount.objects.filter(username=data['username']).exists():
            errors.append('A user of that name already exists, please pick a new username')
            return False

        # Check the password is long enough
        if len(data['password']) < 8:
            errors.append('That password is too short, it must be at least 8 characters long')
            return False

        # Creating and saving the user
        new_user = models.UserAccount(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        new_user.set_password(raw_password=data['password'])
        new_user.save()

        # Create the new Holding
        new_holding = models.Holding(balance=1000, account=new_user)
        new_holding.save()

        return True

    # Are they positing a completed form?
    if request.method == 'POST':
        posted_form = forms.RegisterForm(request.POST)
        if posted_form.is_valid():
            ok = create_new_user(posted_form)

    # Have they logged in?
    if ok:
        pass
    else:
        return render(request, 'default_form.html', {
            'page_title': 'register new user',
            'form': forms.RegisterForm(),
            'errors': errors
        })
