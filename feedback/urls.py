from django.urls import path
from . import views
from .views import delete_feedback

urlpatterns = [
    path('', views.feedbacks, name='feedbacks'),
    path('<int:feedback_number>/', views.feedback, name='feedback'),
    path('submitfeedback/<int:course_pk>/', views.submitfeedback , name='submitfeedback'),
    path('feedback/delete/<int:feedback_number>/', delete_feedback, name='delete_feedback'),
    
]
