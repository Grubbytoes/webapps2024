from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('new_user', views.new_user)
]