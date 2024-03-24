from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from payapp import views

urlpatterns = [
    path('login', csrf_exempt(views.login)),
    path('', csrf_exempt(views.welcome)),
    path('my_account', views.my_account)
]