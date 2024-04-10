from django.shortcuts import render
from . import forms

# Create your views here.
def register(request):
    return render(request, 'register.html', {
        'page_title': 'register new user', 'form': forms.RegisterForm()
    })