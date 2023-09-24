from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedbacks, name='feedbacks'),
    path('<int:feedback_number>/', views.feedback, name='feedback'),
    path('submitfeedback/<int:course_pk>/', views.submitfeedback , name='submitfeedback')
    
]
