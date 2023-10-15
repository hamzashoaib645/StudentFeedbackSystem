from django.shortcuts import render, redirect, get_object_or_404
from .forms import FeedbackForm, ReportMessageForm
from users.models import Student, Teacher, CustomUser, Chairperson, Course
from .models import Feedback , Report
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from collections import Counter
from django.db.models import Count

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'feedback', 'models', 'nlp_model.pkl')
with open(model_path, 'rb') as model_file:
    sentiment_model = pickle.load(model_file)
    
tokenizer_path = os.path.join(BASE_DIR, 'feedback', 'models', 'tokenizer.pickle')
with open(tokenizer_path, 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

    
def analyze_sentiment(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=100)
    predicted_probability = sentiment_model.predict(padded_sequence)[0][0]
    print(f"Predicted Probability for '{text}': {predicted_probability}")
    if 0.3 <= predicted_probability <= 0.7: 
        return 0 
    elif predicted_probability > 0.6:
        return 1
    else:
        return -1

def check_overall_sentiment(sentiments):
    sentiment_counts = Counter(sentiments)
    most_common_sentiment, count = sentiment_counts.most_common(1)[0]
    if len([c for c in sentiment_counts.values() if c == count]) > 1:
        return 0
    
    return most_common_sentiment

def feedbackguide(request):
    return render(request, 'feedback/feedbackguide.html')

@login_required
def feedbacks(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            feedbacks = Feedback.objects.all()
            access = 'admin'
            return render(request, 'feedback/feedbacks.html', {'feedbacks': feedbacks , 'access':access})
        elif request.user.user_role == 'teacher':
            teacher_courses = Course.objects.filter(teacher__username=request.user.username)
            feedbacks = Feedback.objects.filter(course__in=teacher_courses)
            return render(request, 'feedback/tfeedbacks.html', {'feedbacks': feedbacks})
        elif request.user.user_role == 'student':
            student = request.user.username
            feedbacks = Feedback.objects.filter(registration_number=student)
            return render(request, 'feedback/sfeedbacks.html', {'feedbacks': feedbacks})
        else:
            feedbacks = Feedback.objects.all()
            access = 'chairperson'
            return render(request, 'feedback/feedbacks.html', {'feedbacks': feedbacks,'access':access})
    else:
        redirect(login)

@login_required
def exfeedbacks(request, feedback_number):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse("404 Not Found!")
        elif request.user.user_role == 'teacher':
            feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
            return render(request, 'feedback/exteacher_feedback.html', {'feedback': feedback})
        elif request.user.user_role == 'student':
            return HttpResponse("404 Not Found!")
        else:
            return HttpResponse("404 Not Found!")
    else:
        return HttpResponse("404 Not Found!")
    
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
            feedback = get_object_or_404(Feedback, feedback_number=feedback_number)
            access = 'chairperson'
            return render(request, 'feedback/explorefeedback.html', {'feedback': feedback , 'user':access})
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
                    
                    Q1_sentiment = analyze_sentiment(form.cleaned_data['Q1'])
                    print("Q1 Sentiments: ",Q1_sentiment)
                    Q2_sentiment = analyze_sentiment(form.cleaned_data['Q2'])
                    print("Q2 Sentiments: ",Q2_sentiment)
                    Q3_sentiment = analyze_sentiment(form.cleaned_data['Q3'])
                    print("Q3 Sentiments: ",Q3_sentiment)
                    Q4_sentiment = analyze_sentiment(form.cleaned_data['Q4'])
                    print("Q4 Sentiments: ",Q4_sentiment)
                    Q5_sentiment = analyze_sentiment(form.cleaned_data['Q5'])
                    print("Q5 Sentiments: ",Q5_sentiment)
                    
                    overall_sentiment = check_overall_sentiment([Q1_sentiment, Q2_sentiment, Q3_sentiment, Q4_sentiment, Q5_sentiment])
                    print("Overall Sentiments: ",overall_sentiment)
                    
                    # Set the result field in the Feedback model
                    if overall_sentiment == 1:
                        feedback.result = 'Positive'
                    elif overall_sentiment == -1:
                        feedback.result = 'Negative'
                    else:
                        feedback.result = 'Neutral'
                    
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



@login_required
def sentiment_analysis_results(request, serial_number=None, teacher_id=None):
    feedbacks = Feedback.objects.all()
    course_serial = None
    teacher_username = None
    if serial_number:
        feedbacks = feedbacks.filter(course__serial_number=serial_number)
        course_serial = serial_number
    elif teacher_id:
        feedbacks = feedbacks.filter(course__teacher__username=teacher_id)
        teacher_username = teacher_id

    total_feedbacks = feedbacks.count()

    positive_count = feedbacks.filter(result='Positive').count()
    negative_count = feedbacks.filter(result='Negative').count()
    neutral_count = feedbacks.filter(result='Neutral').count()

    positive_percentage = round((positive_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
    negative_percentage = round((negative_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
    neutral_percentage = round((neutral_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0


    # Get distinct courses and teachers for the list
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    user = request.user
    if user.is_superuser:
        access = 'admin'
    elif user.user_role == 'chairperson':
        access = 'chairperson'
    elif user.user_role == 'student':
        return HttpResponse('404 Not Found!')
    else:
        return HttpResponse('404 Not Found!')
    context = {
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'total_feedbacks': total_feedbacks,
        'course_serial' : course_serial,
        'teacher_username' : teacher_username,
        'courses': courses,
        'teachers': teachers,
        'access' : access
    }
    

    return render(request, 'feedback/sentiment_analysis_results.html', context)

@login_required
def submit_report(request, serial_number=None, teacher_id=None):
    feedbacks = Feedback.objects.all()
    user = request.user
    course_serial_number = None  
    teacher_username = None  
    teacher = None
    course = None
    if serial_number:
        feedbacks = feedbacks.filter(course__serial_number=serial_number)
        course_serial_number = serial_number
        course = Course.objects.get(serial_number=serial_number)
    elif teacher_id:
        feedbacks = feedbacks.filter(course__teacher__username=teacher_id)
        teacher_username = teacher_id
        teacher = Teacher.objects.get(username=teacher_id)

    total_feedbacks = feedbacks.count()

    positive_count = feedbacks.filter(result='Positive').count()
    negative_count = feedbacks.filter(result='Negative').count()
    neutral_count = feedbacks.filter(result='Neutral').count()

    positive_percentage = round((positive_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
    negative_percentage = round((negative_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
    neutral_percentage = round((neutral_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0


    # Get distinct courses and teachers for the list
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    
    if user.is_superuser:
        access = 'admin'
    elif user.user_role == 'chairperson':
        access = 'chairperson'
    elif user.user_role == 'student':
        return HttpResponse('404 Not Found!')
    else:
        return HttpResponse('404 Not Found!')
    
    if request.method == 'POST':
        form = ReportMessageForm(request.POST)
        if form.is_valid():
            report_message = form.cleaned_data['report_message']
            feedback_system_user = CustomUser.objects.get(username=user.username)
            # Create Report instance
            report = Report.objects.create(
                username=feedback_system_user,
                user_role=user.user_role,
                positive_percentage=positive_percentage,
                negative_percentage=negative_percentage,
                neutral_percentage=neutral_percentage,
                course_serial_number=course,
                teacher_username=teacher,
                total_feedbacks=total_feedbacks,
                report_message=report_message
            )
            report.save()
            return redirect('dashboard')
    
    form = ReportMessageForm()
    context = {
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'total_feedbacks': total_feedbacks,
        'courses': courses,
        'teachers': teachers,
        'access' : access,
        'form' : form
    }
    

    return render(request, 'feedback/sentiment_report.html', context)

    
@login_required
def teacher_sentiment(request, serial_number=None):
    user = request.user

    if user.user_role == 'teacher':
        # If the user is a teacher, get the courses taught by the teacher
        courses_taught = Course.objects.filter(teacher=user.username)
        course_serial_number = None
        total_feedbacks = positive_count = negative_count = neutral_count = 0
        positive_percentage = negative_percentage = neutral_percentage = 0
        
        if serial_number:
            # If serial_number is provided, filter feedbacks for that specific course
            course = get_object_or_404(Course, serial_number=serial_number)
            feedbacks = Feedback.objects.filter(course=course)
            course_serial_number = serial_number
            
        else:
            # If serial_number is not provided, set values to zero
            feedbacks = Feedback.objects.filter(course__in=courses_taught)
            
        total_feedbacks = feedbacks.count()
        positive_count = feedbacks.filter(result='Positive').count()
        negative_count = feedbacks.filter(result='Negative').count()
        neutral_count = feedbacks.filter(result='Neutral').count()
        
        positive_percentage = round((positive_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        negative_percentage = round((negative_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        neutral_percentage = round((neutral_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        
    else:
        return HttpResponse("404 Not Found!")

    
    context = {
        'courses_taught': courses_taught,
        'selected_course': serial_number,
        'total_feedbacks': total_feedbacks,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'course_serial_number' : course_serial_number,
    }

    return render(request, 'feedback/sentiment_teacher.html', context)

@login_required
def teacher_report(request, serial_number=None):
    user = request.user

    if user.user_role == 'teacher':
        # If the user is a teacher, get the courses taught by the teacher
        courses_taught = Course.objects.filter(teacher=user.username)
        course_serial = None
        teacher = None
        course = None
        course_serial_number = None
        
        total_feedbacks = positive_count = negative_count = neutral_count = 0
        positive_percentage = negative_percentage = neutral_percentage = 0
        
        if serial_number:
            # If serial_number is provided, filter feedbacks for that specific course
            course = get_object_or_404(Course, serial_number=serial_number)
            feedbacks = Feedback.objects.filter(course=course)
            
            
        else:
            # If serial_number is not provided, set values to zero
            feedbacks = Feedback.objects.filter(course__in=courses_taught)
            
        total_feedbacks = feedbacks.count()
        positive_count = feedbacks.filter(result='Positive').count()
        negative_count = feedbacks.filter(result='Negative').count()
        neutral_count = feedbacks.filter(result='Neutral').count()
        
        positive_percentage = round((positive_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        negative_percentage = round((negative_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        neutral_percentage = round((neutral_count / total_feedbacks) * 100) if total_feedbacks > 0 else 0
        
    else:
        return HttpResponse("404 Not Found!")

    if request.method == 'POST':
        form = ReportMessageForm(request.POST)
        if form.is_valid():
            report_message = form.cleaned_data['report_message']
            feedback_system_user = CustomUser.objects.get(username=user.username)
            # Create Report instance
            report = Report.objects.create(
                username=feedback_system_user,
                user_role=user.user_role,
                positive_percentage=positive_percentage,
                negative_percentage=negative_percentage,
                neutral_percentage=neutral_percentage,
                course_serial_number=course,
                teacher_username=teacher,
                total_feedbacks=total_feedbacks,
                report_message=report_message
            )
            report.save()
            return redirect('dashboard')
    
    form = ReportMessageForm()
    
    context = {
        'courses_taught': courses_taught,
        'selected_course': serial_number,
        'total_feedbacks': total_feedbacks,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'course_serial_number' : course_serial_number,
        'form' : form,
    }

    return render(request, 'feedback/teacher_report.html', context)

@login_required
def view_report(request):
    if request.user.is_authenticated:
        reports = Report.objects.all()
        if request.user.is_superuser:
            access = 'admin'
            return render(request, 'feedback/view_report.html', {'reports': reports , 'access':access})
        elif request.user.user_role == 'teacher':
            return HttpResponse("404 Not Found!")
        elif request.user.user_role == 'student':
            return HttpResponse("404 Not Found!")
        else:
            access = 'chairperson'
            return render(request, 'feedback/view_report.html', {'reports': reports,'access':access})
    else:
        redirect(login)
        
@login_required
def explore_report(request, report_number):
    if request.user.is_authenticated:
        if report_number:
            reports = get_object_or_404(Report, report_number=report_number)
        else:
            print('No report Found!')
        if request.user.is_superuser:
            access = 'admin'
            return render(request, 'feedback/explore_report.html', {'reports': reports , 'access':access})
        elif request.user.user_role == 'teacher':
            return HttpResponse("404 Not Found!")
        elif request.user.user_role == 'student':
            return HttpResponse("404 Not Found!")
        else:
            access = 'chairperson'
            return render(request, 'feedback/explore_report.html', {'reports': reports,'access':access})
    else:
        redirect(login)