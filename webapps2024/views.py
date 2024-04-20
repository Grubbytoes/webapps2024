from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Non-view functions
def default_context(request, page_title: str) -> dict:
    context = {
        'page_title': page_title,
        'logged_in': request.user.is_authenticated,
        'user': request.user
    }
    return context

def home(request):
    # Variables
    context = default_context(request, "home")

    return render(request, 'home.html', context)


def do_logout(request):
    logout(request)
    return redirect('/home')