from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Non-view functions
def default_context(_request, page_title: str) -> dict:
    context = {
        'page_title': page_title,
        'logged_in': _request.user.is_authenticated,
        'user': _request.user
    }
    return context

def home(request):
    # Variables
    context = default_context(request, "home")

    return render(request, 'home.html', context)


def do_logout(request):
    logout(request)
    return redirect('/home')