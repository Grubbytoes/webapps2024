from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from globaltools import forms as myforms
import globaltools.viewmaster as vm


NAVIGATION = [
    ('home', '/payapp'),
    ('login', '/payapp/login'),
    ('secret', 'https://en.wikipedia.org/wiki/Rickrolling')
]
# Create your views here.
## ... Isn't this exactly the scenario where wrappers would be useful...?
def login(request: HttpRequest):
    login_core  = vm.FormView("login", "payapp/login.html", myforms.LoginForm())
    login_core.update_context({'navigation': NAVIGATION})
    return login_core.view(request)

def welcome(request: HttpRequest):
    welcome_core = vm.ViewMaster("welcome", "payapp/welcome.html")
    welcome_core.update_context({'navigation': NAVIGATION})
    return welcome_core.view(request)

def my_account(request: HttpRequest):
    my_account_core = vm.ViewMaster("my account", "payapp/my_account.html")
    my_account_core.require_login('/payapp')
    return my_account_core.view(request)