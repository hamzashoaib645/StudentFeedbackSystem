from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm
from users.models import Student, Teacher, CustomUser, Chairperson
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def feedbacks(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            feedbacks = Feedback.objects.all()
            return render(request, 'feedback/feedbacks.html', {'feedbacks': feedbacks})
        elif request.user.user_role == 'teacher':
            feedbacks = Feedback.objects.all()
            return render(request, 'feedback/tfeedbacks.html', {'feedbacks': feedbacks})
        elif request.user.user_role == 'student':
            student = request.user.username
            feedbacks = Feedback.objects.filter(registration_number=student)
            return render(request, 'feedback/sfeedbacks.html', {'feedbacks': feedbacks})
        else:
            feedbacks = Feedback.objects.all()
            return render(request, 'feedback/cfeedbacks.html', {'feedbacks': feedbacks})
    else:
        redirect(login)

@login_required
def feedback(request, feedback_number):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
            access = 'admin'
            return render(request, 'feedback/explorefeedback.html', {'feedback': feedback , 'user':access})
        elif request.user.user_role == 'teacher':
            feedbacks = Feedback.objects.all()
            return render(request, 'feedback/tfeedbacks.html', {'feedbacks': feedbacks})
        elif request.user.user_role == 'student':
            feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
            if feedback.registration_number.registration_number == request.user.username:
                access = 'student'
                return render(request, 'feedback/explorefeedback.html', {'feedback': feedback , 'user':access})
            else:
                return redirect('feedbacks')
        else:
            feedbacks = Feedback.objects.all()
            return render(request, 'feedback/cfeedbacks.html', {'feedbacks': feedbacks})
    else:
        redirect(login)
        
    user = request.user
    access = user.user_role
    feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
    return render(request, 'feedback/explorefeedback.html', {'feedback': feedback , 'user':access})

@login_required
def submitfeedback(request, course_pk):
    if request.user.is_authenticated:
        if request.user.user_role == 'student':
            student = Student.objects.get(registration_number=request.user.username)
            course = student.enrolled_courses.get(pk=course_pk)

            if request.method == 'POST':
                form = FeedbackForm(request.POST, course=course) 
                if form.is_valid():
                    feedback = form.save(commit=False)
                    feedback.registration_number = student
                    feedback.course = course
                    feedback.save()
                    student.enrolled_courses.filter(pk=course_pk).update(feedback=True)
                    return redirect('feedbacks')
            else:
                form = FeedbackForm(course=course)  # Pass the course to the form

            context = {
                'form': form,
                'course': course,
            }
            return render(request, 'feedback/submit_feedback.html', context)
        else:
            return HttpResponse("404 Not Found!")
    else:
        return redirect('login')
    
@login_required
def delete_feedback(request, feedback_number):
    feedback = get_object_or_404(Feedback, feedback_number=feedback_number)

    if request.method == 'POST':
        feedback.delete()
        return redirect('feedbacks')  # Redirect to feedback list page after deletion

    return render(request, 'feedback/delete_feedback.html', {'feedback': feedback})