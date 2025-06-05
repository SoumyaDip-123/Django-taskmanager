from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Task

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth', 'gender')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
