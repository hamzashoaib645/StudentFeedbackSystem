from django.db import models
from users.models import Student, Course, CustomUser, Teacher

class Feedback(models.Model):
    RESULT_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    ]
    feedback_number = models.AutoField(primary_key=True)
    registration_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    date_submit_time = models.DateTimeField(auto_now_add=True)
    Q1 = models.CharField(max_length=150, null=True)
    Q2 = models.CharField(max_length=150, null=True)
    Q3 = models.CharField(max_length=150, null=True)
    Q4 = models.CharField(max_length=150, null=True)
    Q5 = models.CharField(max_length=150, null=True)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True)
    
    def __str__(self):
        return f"Feedback #{self.feedback_number} - Course: {self.course.course_name} by {self.registration_number}"
    
class Report(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('chairperson', 'Chairperson'),
    )
    
    report_number = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    positive_percentage = models.FloatField()
    negative_percentage = models.FloatField()
    neutral_percentage = models.FloatField()
    course_serial_number = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    teacher_username = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    total_feedbacks = models.IntegerField()
    report_message = models.TextField()

    def __str__(self):
        return f"Report for {self.username.username} - Course: {self.course_serial_number} - Teacher: {self.teacher_username}"


