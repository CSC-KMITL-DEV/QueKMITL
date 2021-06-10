from django.contrib import auth
from django.urls import path

from . import views


urlpatterns = [
    path('department', views.department, name='department'),
    path('forms', views.forms, name='forms'),
    path('view_que/', views.view_que, name='view_que'),
    path('info_que/<int:id>/', views.info_que, name='info_que'),
    path('close_que/<int:id>/', views.close_que, name='close_que'),
   
]