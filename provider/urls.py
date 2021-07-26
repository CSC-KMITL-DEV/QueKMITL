from django.contrib import auth
from django.urls import path

from . import views


urlpatterns = [
    path('department', views.department, name='department'),
    path('department/create_dep', views.create_dep, name='create_dep'),
    path('department/type_in_dep/<int:id>', views.type_in_dep, name='type_in_dep'),
    path('department/type_in_dep/<int:id>/create_type_in_dep/', views.create_type_in_dep, name='create_type_in_dep'),
    path('type_in_dep/<int:id>/view_que/', views.view_que, name='view_que'),
    path('type_in_dep/<int:id>/forms/', views.forms, name='forms'),
    path('info_que/<int:id>/', views.info_que, name='info_que'),
    path('info_que/<int:id>/userbook', views.userbook, name='userbook'),
    path('info_que/<int:id>/create_walkin', views.create_walkin, name='create_walkin'),
    path('close_que/<int:id>/', views.close_que, name='close_que'),
    path('using/<int:id>/', views.using, name='using'),    
    path('success/<int:id>/', views.success, name='success'), 
    path('putoff/<int:id>/', views.putoff, name='putoff'),     
    path('delete/<int:id>/', views.delete, name='delete'),    
    path('cancel/<int:id>/', views.cancel, name='cancel'),    
    path('using_walkin/<int:id>/', views.using_walkin, name='using_walkin'),    
    path('success_walkin/<int:id>/', views.success_walkin, name='success_walkin'),  
    path('delete_walkin/<int:id>/', views.delete_walkin, name='delete_walkin'),    
    path('show_que', views.show_que, name='show_que'),
  

]