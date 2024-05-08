from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversion_request)
]