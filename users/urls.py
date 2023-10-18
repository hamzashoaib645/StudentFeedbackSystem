# users/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/submissions/', views.submissionlist, name='submissions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('dashboard/courses/', views.courses, name='courses'),
    path('dashboard/addcourse/', views.addcourse, name='addcourse'),
    path('dashboard/addteacher/', views.addteacher, name='addteacher'),
    path('dashboard/addchairperson/', views.addchairperson, name='addchairperson'),
    path('dashboard/addstudent/', views.addstudent, name='addstudent'),
    path('contact/', views.contact, name='contact'),
    path('student/delete/<str:registration_number>/', views.delete_student, name='delete_student'),
    path('teacher/delete/<str:username>/', views.delete_teacher, name='delete_teacher'),
    path('chairperson/delete/<str:username>/', views.delete_chairperson, name='delete_chairperson'),
    path('course/delete/<int:serial_number>/', views.delete_course, name='delete_course'),
    #path('dashboard/students/', views.students, name='teachers'),
    # Add other URLs as needed
]
