from django.shortcuts import render, redirect
from .forms import FeedbackForm
from users.models import Student

def submitfeedback(request, course_pk):
    student = Student.objects.get(registration_number=request.user.username)
    course = student.enrolled_courses.get(pk=course_pk)

    if request.method == 'POST':
        form = FeedbackForm(request.POST, course=course)  # Pass the course to the form
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.registration_number = student
            feedback.course = course
            feedback.save()
            # Update the student's feedback status to indicate that they have submitted feedback for this course
            student.enrolled_courses.filter(pk=course_pk).update(feedback=True)
            return redirect('dashboard')
    else:
        form = FeedbackForm(course=course)  # Pass the course to the form

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'feedback/submit_feedback.html', context)