# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('chairperson', 'Chairperson'),
    )

    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.full_name}) - {self.department}"
    
class Course(models.Model):
    serial_number = models.AutoField(primary_key=True, unique=True)
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=255)
    section = models.PositiveIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.course_id} - {self.course_name} (Section {self.section}) teached by {self.teacher}"
    
class Student(models.Model):
    full_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20, unique=True, primary_key=True)
    password = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    enrolled_courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        enrolled_courses_str = ", ".join([f" {course.course_name} - {course.section}" for course in self.enrolled_courses.all()])
        return f"{self.full_name} - Semester: {self.semester} ({self.registration_number}) enrolled in: {enrolled_courses_str}"

class Chairperson(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}"
    
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"