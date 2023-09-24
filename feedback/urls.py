from django.urls import path
from . import views

urlpatterns = [
    path('', views.submitfeedback, name='home'),
    path('submitfeedback/<int:course_pk>/', views.submitfeedback , name='submitfeedback')
    
]
