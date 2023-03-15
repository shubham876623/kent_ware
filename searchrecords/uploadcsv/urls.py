
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Input_File_upload, name='index'),
]