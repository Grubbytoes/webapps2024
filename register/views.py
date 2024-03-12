from django.http import HttpResponse
from django.shortcuts import render
from . import forms


def new_user(request):
    context = {'page_title': 'register', 'form': forms.RegisterForm()}
    return render(request, 'register/new_user.html', context)
