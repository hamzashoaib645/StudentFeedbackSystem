from django.urls import path
from . import views
from .views import delete_feedback

urlpatterns = [
    path('', views.feedbacks, name='feedbacks'),
    path('<int:feedback_number>/', views.feedback, name='feedback'),
    path('submitfeedback/<int:course_pk>/', views.submitfeedback , name='submitfeedback'),
    path('feedback/delete/<int:feedback_number>/', delete_feedback, name='delete_feedback'),
    path('feedbackguide/', views.feedbackguide, name='feedbackguide'),
    path('teacher/', views.feedbacks, name='teacherfeedback'),
    path('teacher/<int:feedback_number>/', views.exfeedbacks, name='teacherfeedbackexp'),
    path('teacher/sentiment/', views.teacher_sentiment, name='teacheranalysis'),
    path('teacher/sentiment/<int:serial_number>/', views.teacher_sentiment, name='teacheranalysiscourse'),
    path('teacher/report', views.teacher_report, name='teacherreport'),
    path('teacher/report/<int:serial_number>/', views.teacher_report, name='teacherareportcourse'),
    path('sentiment-analysis/', views.sentiment_analysis_results, name='sentiment_analysis_results'),
    path('sentiment-analysis/course/<int:serial_number>/', views.sentiment_analysis_results, name='course_sentiment_analysis'),
    path('sentiment-analysis/teacher/<str:teacher_id>/', views.sentiment_analysis_results, name='teacher_sentiment_analysis'),
    path('report/', views.submit_report, name='sentiment_report'),
    path('report/course/<int:serial_number>/', views.submit_report, name='course_sentiment_report'),
    path('report/course/<str:teacher_id>/', views.submit_report, name='teacher_sentiment_report'),
    path('report/teacher/', views.view_report, name='view_reports'),
    path('report/teacher/<int:report_number>/', views.explore_report, name='explore_reports'),
]
