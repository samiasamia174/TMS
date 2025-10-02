# File: accounts/forms.py
# Complete fixed version

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'user_type', 'password1', 'password2']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'student_id',  # FIXED: Changed from user_id to student_id
            'department',
            'address',
            'profile_picture',
            'date_of_birth',
            'emergency_contact'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student/Staff ID'}),  # FIXED
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact'}),
        }
        labels = {
            'full_name': 'Full Name',
            'student_id': 'ID Number',  # FIXED: Changed label
            'department': 'Department',
            'address': 'Address',
            'profile_picture': 'Profile Picture',
            'date_of_birth': 'Date of Birth',
            'emergency_contact': 'Emergency Contact',
        }