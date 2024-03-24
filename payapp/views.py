from django.http import HttpResponse
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

login = vm.FormView("login", "payapp/login.html", myforms.LoginForm())
login.update_context({'navigation': NAVIGATION})

welcome = vm.ViewMaster("welcome", "payapp/welcome.html")
welcome.update_context({'navigation': NAVIGATION})

my_account = vm.ViewMaster("my account", "payapp/my_account.html")
my_account.require_login('/payapp')