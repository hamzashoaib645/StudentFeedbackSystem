from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from .models import Course , Teacher, Student


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'custom-password-class'}),
        required=True
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'custom-password-class'}),
        required=True
    )
    
    profile_picture = forms.ImageField(required=False)


    class Meta:
        model = CustomUser
        fields = ('username', 'user_role')
        
    widgets = {
        'user_role': forms.Select(attrs={'class': 'new-user-role'}),
    }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match." , code='password_mismatch')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Exclude 'admin' from the choices in the 'User Role' field
        self.fields['user_role'].choices = [
            choice for choice in self.fields['user_role'].choices if choice[0] != 'admin'
        ]


class CustomAuthenticationForm(forms.Form):  # Inherit from AuthenticationForm
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'custom-username-class'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'custom-password-class'}),
    )


class CustomProfileForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'custom-password-class'}),
        required=False  # We make this field optional
    )

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs.update({'class': 'custom-profile-pic-class'})
        self.fields['password'].widget.attrs.update({'class': 'custom-password-class'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super(CustomProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class CoursesForm(forms.ModelForm):
    num_sections = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 6)])

    class Meta:
        model = Course
        fields = ['course_id', 'course_name' ]
        


class TeachersForm(forms.ModelForm):
    # Add a field to select multiple courses where the teacher is None
    unassigned_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.filter(teacher__isnull=True),
        required=False,  # This allows not selecting any courses
        widget=forms.CheckboxSelectMultiple,
        label="Select Courses (Unassigned)"
    )
    role = forms.CharField(widget=forms.HiddenInput(), initial="teacher")
    DEPARTMENT_CHOICES = (
        ('cs', 'Computer Science'),
        ('se', 'Software Engineering'),
        ('acs', 'Applied Computer Science'),
        ('other', 'Other'),
    )
    
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    class Meta:
        model = Teacher
        fields = ['full_name', 'username', 'password', 'department']
        widgets = {
            'password': forms.PasswordInput(),
        }

class TeacherProfileForm(forms.ModelForm):
    # Define the form fields you want to display and modify
    full_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100, disabled=True)  # Disable the username field
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=False)
    DEPARTMENT_CHOICES = (
        ('cs', 'Computer Science'),
        ('se', 'Software Engineering'),
        ('acs', 'Applied Computer Science'),
        ('other', 'Other'),
    )
    
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)

    class Meta:
        model = Teacher
        fields = ['full_name', 'username', 'password', 'confirm_password', 'department']

class StudentForm(forms.ModelForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial="student")
    SEMESTER_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8')
    )
    
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES)
    class Meta:
        model = Student
        fields = ['full_name', 'registration_number', 'password', 'semester', 'enrolled_courses']

    enrolled_courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Students can choose not to enroll in any courses initially
    )

