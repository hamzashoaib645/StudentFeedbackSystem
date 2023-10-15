from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib import messages
from .forms import CustomProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Teacher , Course, Student, Chairperson, ContactSubmission
from .forms import TeachersForm, CoursesForm, StudentForm, TeacherProfileForm, ChairpersonForm, ContactForm
from django.contrib.auth.hashers import make_password

def home(request):
    if request.user.is_authenticated:
        loginyes = True
    else:
        loginyes = False
        
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/submission.html',{'access':loginyes})
    else:
        form = ContactForm()
    return render(request, 'dashboard/home.html', {'form': form, 'access':loginyes})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/submission.html')
    else:
        form = ContactForm()
    return render(request, 'users/contact.html',{'form':form})

@login_required
def submissionlist(request):
    user = request.user
    if user.is_superuser:
        contact= ContactSubmission.objects.all()
        return render(request, 'dashboard/submissionlist.html', {'contact':contact})
    else:
        return HttpResponse("404 Not Found!")
    

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/../dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    if user.user_role == 'teacher':
        # Get the logged-in teacher's username
        logged_in_username = request.user.username

        # Fetch the teacher's data using their username
        try:
            teacher = Teacher.objects.get(username=logged_in_username)
        except Teacher.DoesNotExist:
            # Handle the case where the teacher doesn't exist
            return redirect('login')  # Redirect to the login page or another appropriate page

        if request.method == "POST":
            # Check if the teacher is updating their password
            form = TeacherProfileForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data.get('password')
                confirm_password = form.cleaned_data.get('confirm_password')

                if new_password and new_password == confirm_password:
                    # Update the password if provided and confirmed
                    teacher.password = new_password

                # Update other fields
                teacher.full_name = form.cleaned_data['full_name']
                teacher.department = form.cleaned_data['department']
                teacher.save()

                # Redirect to a success page or another appropriate page
                return redirect('profile')  # You can replace 'profile' with the URL name for the profile page

        else:
            # Pre-fill the form with the teacher's existing data
            form = TeacherProfileForm(instance=teacher)
        
        context = {'form': form}
        return render(request, 'users/profile.html', context)    

    return render(request, 'users/profile.html')

        

@login_required
def addcourse(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            form = CoursesForm(request.POST)
            if form.is_valid():
                course_id = form.cleaned_data['course_id']
                course_name = form.cleaned_data['course_name']
                num_sections = int(form.cleaned_data['num_sections'])

                for section in range(1, num_sections + 1):
                    Course.objects.create(course_id=course_id, course_name=course_name, section=section)

                return redirect('addcourse')  # Redirect to a course list view
        else:
            form = CoursesForm()
            
        courses = Course.objects.all()
        context = {
                    'courses': courses,
                    'form' : form
                }
        return render(request, 'dashboard/addcourse.html', context)
    else:
        return HttpResponse("404 Not Found!")

@login_required
def addteacher(request):
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            form = TeachersForm(request.POST)
            if form.is_valid():
            # Save the teacher without committing to the database
                username1 = form.cleaned_data['username']
                password1 = form.cleaned_data['password']
                role = form.cleaned_data['role']
            
                teacher = form.save(commit=False)
                hashed_password = make_password(password1)
            # Save the teacher instance to get the primary key (username)
                teacher.save()
            
            # Get the selected courses from the form
                selected_courses = form.cleaned_data.get('unassigned_courses')
            
                custom_user = CustomUser(username=username1, password=hashed_password, user_role=role)
                custom_user.save()
            # Assign the teacher to the selected courses
                for course in selected_courses:
                    course.teacher = teacher
                    course.save()
            
            # Redirect to a success page or wherever you want
                return redirect('addteacher')
        else:
            form = TeachersForm()
        teachers = Teacher.objects.all()
        context = {'form': form,
               'teachers': teachers}
        return render(request, 'dashboard/addteacher.html', context)
    else:
        return HttpResponse("404 Not Found!")


@login_required
def addstudent(request):
    user = request.user
    if user.is_superuser:
        if request.method == 'POST':
            form = StudentForm(request.POST)
            if form.is_valid():
                # Save the student instance with selected courses
                student = form.save()

                # Create a CustomUser instance for the student
                username1 = form.cleaned_data['registration_number']
                password1 = form.cleaned_data['password']
                role = form.cleaned_data['role']
                hashed_password = make_password(password1)
                custom_user = CustomUser(username=username1, password=hashed_password, user_role=role)
                custom_user.save()

                return redirect('addstudent')  # Redirect to a page displaying a list of students
        else:
            form = StudentForm()

        students = Student.objects.all()
        context = {'form': form, 'students': students}
        return render(request, 'dashboard/addstudent.html', context)
    else:
        return HttpResponse("404 Not Found!")

@login_required
def addchairperson(request):
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            form = ChairpersonForm(request.POST)
            if form.is_valid():
                # Save the chairperson without committing to the database
                username1 = form.cleaned_data['username']
                password1 = form.cleaned_data['password']
                role = form.cleaned_data['role']

                # Hash the password
                hashed_password = make_password(password1)

            # Save the chairperson instance to get the primary key (username)
                chairperson = Chairperson(username=username1, password=hashed_password, full_name=form.cleaned_data['full_name'])
                chairperson.save()

            # Create a CustomUser instance for the chairperson
                custom_user = CustomUser(username=username1, password=hashed_password, user_role=role)
                custom_user.save()

                # Redirect to a success page or wherever you want
                return redirect('addchairperson')
        else:
            form = ChairpersonForm()

        chairpersons = Chairperson.objects.all()
        context = {'form': form, 'chairpersons': chairpersons}
        return render(request, 'dashboard/addchairperson.html', context)
    else:
        return HttpResponse("404 Not Found!")

@login_required
def dashboard(request):
    user = request.user  

    if user.is_superuser:
        return admin_dashboard(request)
    elif user.user_role == 'teacher':
        return teacher_dashboard(request)
    elif user.user_role == 'student':
        return student_dashboard(request)
    elif user.user_role == 'chairperson':
        return chairperson_dashboard(request)
    
    return render(request, 'users/register.html', {'user': user})

def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')

def student_dashboard(request):
    student = Student.objects.get(registration_number=request.user.username)

    # Get the list of enrolled courses for the student
    enrolled_courses = student.enrolled_courses.filter(feedback__isnull=False)

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses,
    }

    return render(request, 'dashboard/student_dashboard.html', context)
    
def teacher_dashboard(request):
    teacher = Teacher.objects.get(username=request.user.username)
    name = teacher.full_name
    return render(request, 'dashboard/teacher_dashboard.html', {'name': name})

def chairperson_dashboard(request):
    chairperson = Chairperson.objects.get(username=request.user.username)
    name = chairperson.full_name
    return render(request, 'dashboard/chairperson_dashboard.html', {'name': name})