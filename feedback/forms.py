from django import forms
from .models import Feedback, Report

class FeedbackForm(forms.ModelForm):
    RESULT_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    ]

    result = forms.ChoiceField(
        widget=forms.HiddenInput(),
        choices=RESULT_CHOICES,
        initial='Neutral',
    )
    class Meta:
        model = Feedback
        fields = ['course', 'Q1' , 'Q2', 'Q3', 'Q4', 'Q5','result']

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)  # Get the course from kwargs
        super(FeedbackForm, self).__init__(*args, **kwargs)
        if course:
            self.fields['course'].initial = course  # Set the initial value of the course field
            
class ReportMessageForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_message']

    def __init__(self, *args, **kwargs):
        super(ReportMessageForm, self).__init__(*args, **kwargs)