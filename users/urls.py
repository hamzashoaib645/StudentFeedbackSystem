# users/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('dashboard/courses/', views.courses, name='courses'),
    path('dashboard/addcourse/', views.addcourse, name='addcourse'),
    path('dashboard/addteacher/', views.addteacher, name='addteacher'),
    #path('dashboard/teachers/', views.teachers, name='teachers'),
    path('dashboard/addstudent/', views.addstudent, name='addstudent'),
    #path('dashboard/students/', views.students, name='teachers'),
    # Add other URLs as needed
]
