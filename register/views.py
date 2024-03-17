from django.http import HttpResponse, Http404
from django.shortcuts import render
from globaltools import models, forms


def new_user(request):
    context = {'page_title': 'register', 'form': forms.RegisterForm()}
    if request.method == "GET":
        return render(request, 'register/new_user.html', context)
    elif request.method == "POST":
        form = forms.RegisterForm(request.POST)
        feilds = form.data

        # Check the form is valid
        vaild: bool = True
        if not form.is_valid():
            context['message'] = "Sorry, bad for posted - try again"
            render(request, 'register/new_user.html', context)

        new_account_code = models.UserAccount.create_new(new_username, new_password, new_email)
        if new_account_code > 0:
            return HttpResponse("<p>Account created successfully</p>")
        elif new_account_code == -1:
            context['message'] = "Sorry, that username is already taken - try again"
        else:
            context['message'] = "Sorry, that username is already taken - try again"
        return render(request, 'register/new_user.html', context)
    else:
        raise Http404()
