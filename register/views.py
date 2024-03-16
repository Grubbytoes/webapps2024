from django.http import HttpResponse, Http404
from django.shortcuts import render
from . import forms, models


def new_user(request):
    context = {'page_title': 'register', 'form': forms.RegisterForm()}
    if request.method == "GET":
        return render(request, 'register/new_user.html', context)
    elif request.method == "POST":
        feilds = forms.RegisterForm(request.POST)
        # Check the form is valid
        if not feilds.is_valid():
            return HttpResponse("Error: bad form")

        # Saving the new account
        new_username, new_password = feilds.data['username'], feilds.data['password']
        new_account: models.Account = models.account_factory(new_username, new_password)
        new_account.email = feilds.data['email']
        new_account.save()

        return HttpResponse("<p>Sorry, WIP lol</p>")
    else:
        raise Http404()
