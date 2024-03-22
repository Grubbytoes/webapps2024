from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from globaltools import forms as myforms


# Create your views here.
@csrf_exempt
def login(request):
    login_context = {
        'page_title': 'login',
        'form': myforms.LoginForm()
    }

    if request.method == "GET":
        return render(request, 'payapp/login.html', login_context)
    elif request.method == "POST":
        form = myforms.LoginForm(request.POST)
        id_token: int

        if form.is_valid():
            id_token = form.authenticate_user()
        else:
            id_token = -1

        if id_token >= 0:
            request.session["id"] = id_token
            return HttpResponse("You're in!")
        else:
            return HttpResponse("Didn't work!")

