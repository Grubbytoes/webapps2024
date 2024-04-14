from django.contrib.auth import logout
from django.shortcuts import render, redirect


def home(request):
    # Variables
    context = {
        'page_title': "Home",
        'logged_in':  request.user.is_authenticated
    }

    return render(request, 'home.html', context)


def do_logout(request):
    logout(request)
    return redirect('/home')