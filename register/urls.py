from django.urls import path
from . import views

urlpatterns = [
    path('', views.register),
    path('setup', views.setup),
    path('make_user', views.make_user)
]