from django.shortcuts import render

from payapp import forms


# Create your views here.
def login(request):
    login_context = {
        'page_title': 'login',
        'form': forms.LoginForm()
    }

    return render(request, 'payapp/login.html', login_context)
