from django.shortcuts import render
from . import forms
from payapp import models

# Create your views here.
def register(request):
    # The variables we will use
    logged_in_ok = False

    # Internal methods we will use
    def create_new_user(form_) -> bool:
        # Get the data from the form
        data = form_.cleaned_data

        # Creating and saving the user
        new_user = models.UserAccount(
            username=data['username'],
            email=data['email'],
            first_name= data['first_name'],
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
            logged_in_ok = create_new_user(posted_form)


    # Have they logged in?
    if logged_in_ok:
        pass
    else:
        return render(request, 'register.html', {
            'page_title': 'register new user', 'form': forms.RegisterForm()
        })
