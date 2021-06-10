from django.contrib import auth
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.index_page, name='index'),
    path('login/', views.login_page, name='login'),
    path('check_login/', views.check_login, name='check_login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.logout_page, name='logout'),
   
]