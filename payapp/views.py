from django.contrib.auth import authenticate
from django.shortcuts import render
from . import forms

# Create your views here.
def login(request):
    if request.method == "POST":
        posted_form = forms.LoginForm(request.POST)
        posted_form_data = posted_form.cleaned_data
        logged_in_user = authenticate(posted_form_data['username'], posted_form_data['password'])

        if logged_in_user is not None:
            print("YOU'RE IN!!")
    else:
        return render(request, 'login.html', {'page_title': 'login', 'form': forms.LoginForm()})
