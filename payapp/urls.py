from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('logout', views.logout),
    path('make_payment', views.make_payment),
    path('request_payment', views.request_payment),
    path('my_account', views.my_account)
]
