from django.contrib import admin
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Course, Teacher, Student, Chairperson
User = get_user_model()

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Chairperson)

# Register your models here.
admin.site.site_header = "Student Feedback System"