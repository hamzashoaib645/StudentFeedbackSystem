from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['course', 'Q1' , 'Q2', 'Q3', 'Q4', 'Q5']

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)  # Get the course from kwargs
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['course'].initial = course  # Set the initial value of the course field
            