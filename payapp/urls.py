from django.urls import path

from payapp import views

urlpatterns = [
    path('login', views.login),
    path('', views.welcome.view)
]