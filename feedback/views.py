from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from users.models import Student
from .models import Feedback

def feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/feedbacks.html', {'feedbacks': feedbacks})

def feedback(request, feedback_number):
    feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
    return render(request, 'feedback/explorefeedback.html', {'feedback': feedback})

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
            return redirect('feedbacks')
    else:
        form = FeedbackForm(course=course)  # Pass the course to the form

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'feedback/submit_feedback.html', context)