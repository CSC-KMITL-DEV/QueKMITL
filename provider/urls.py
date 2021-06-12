from django.contrib import auth
from django.urls import path

from . import views


urlpatterns = [
    path('department', views.department, name='department'),
    path('department/create_dep', views.create_dep, name='create_dep'),
    path('department/<int:id>/type_in_dep/', views.type_in_dep, name='type_in_dep'),
    path('department/<int:id>/type_in_dep/create_type_in_dep/', views.create_type_in_dep, name='create_type_in_dep'),
    path('type_in_dep/<int:id>/view_que/', views.view_que, name='view_que'),
    path('type_in_dep/<int:id>/forms/', views.forms, name='forms'),

    path('info_que/<int:id>/', views.info_que, name='info_que'),
    path('close_que/<int:id>/', views.close_que, name='close_que'),
   
]