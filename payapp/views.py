from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import forms, models


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == "POST":
        # If the form is invalid, exit.
        # Otherwise, get the data
        posted_form = forms.LoginForm(request.POST)
        if not posted_form.is_valid():
            return
        posted_form_data = posted_form.cleaned_data

        # Try and find a user of the right name, and authenticate their password
        query = models.UserAccount.objects.filter(username=posted_form_data['username'])
        if query is None:
            return
        user_by_name: models.UserAccount = query[0]
        if not user_by_name.check_password(posted_form_data['password']):
            return

        print('beep')
    else:
        return render(request, 'login.html', {'page_title': 'login', 'form': forms.LoginForm()})
