from django.http import HttpResponse
from django.template import loader


def home(request):
    context = {
        'page_title': 'home'
    }

    page = loader.get_template('webapps2024/home.html')
    return HttpResponse(page.render(context))