from django.shortcuts import render
from . import forms
from payapp import models

# Create your views here.
def register(request):
    # The variables we will use
    logged_in_ok = False
    posted_form = None

    # Are they getting the form, or positing a completed form?
    if request.method == 'POST':
        posted_form = forms.RegisterForm(request.POST)
        if posted_form.is_valid():
            # Get the data from the form
            data = posted_form.cleaned_data
            new_username = data['username']
            new_raw_password = data['password']

            # Creating and saving the user
            new_user = models.UserAccount(username=new_username)
            new_user.set_password(raw_password=new_raw_password)
            new_user.save()


    else: # Safe to assume == 'GET'
        pass


    return render(request, 'register.html', {
        'page_title': 'register new user', 'form': forms.RegisterForm()
    })