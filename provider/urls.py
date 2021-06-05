from django.contrib import auth
from django.urls import path

from . import views


urlpatterns = [
    path('', views.forms, name='forms'),
    path('view_que/', views.view_que, name='view_que'),
    path('info_que/<int:id>/', views.info_que, name='info_que'),
   
]