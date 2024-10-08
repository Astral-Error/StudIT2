from django import forms
from django.contrib.auth.models import User
from .models import Student

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    registration_no = forms.CharField(max_length=100, required=True)
    branch_choices = [
        ('CSE Core', 'CSE Core'),
        ('CSE+Spec', 'CSE+Spec'),
        ('ECE', 'ECE'),
        ('EEE', 'EEE'),
        ('Mechanical', 'Mechanical'),
        ('Civil', 'Civil'),
        ('Biotechnology', 'Biotechnology'),
    ]
    branch = forms.ChoiceField(choices=branch_choices, required=True)
    enrollment_year = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['registration_no', 'enrollment_year', 'branch']
