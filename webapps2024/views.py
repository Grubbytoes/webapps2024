from django.shortcuts import render


def home(request):
    # Variables
    context = {
        'page_title': "Home",
        'logged_in':  request.user.is_authenticated
    }

    return render(request, 'home.html', context)
