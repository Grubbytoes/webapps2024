from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('logout', views.logout),
    path('make_payment', views.make_payment),
    path('request_payment', views.request_payment),
    path('my_account', views.my_account),
    path('my_notifications', csrf_exempt(views.my_notifications)),
    path('my_payments', csrf_exempt(views.my_payments)),
    path('my_requests', csrf_exempt(views.my_requests))
]
