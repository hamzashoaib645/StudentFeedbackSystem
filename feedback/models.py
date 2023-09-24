from django.db import models
from users.models import Student, Course

class Feedback(models.Model):
    feedback_number = models.AutoField(primary_key=True)
    registration_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    date_submit_time = models.DateTimeField(auto_now_add=True)
    Q1 = models.CharField(max_length=50, null=True)
    Q2 = models.CharField(max_length=50, null=True)
    Q3 = models.CharField(max_length=50, null=True)
    Q4 = models.CharField(max_length=50, null=True)
    Q5 = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"Feedback #{self.feedback_number} - Course: {self.course.course_name} by {self.registration_number}"
