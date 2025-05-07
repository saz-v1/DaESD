from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@live\.uwe\.ac\.uk$',
                message='Please use your UWE email address (@live.uwe.ac.uk)',
                code='invalid_email'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@live.uwe.ac.uk'):
            raise forms.ValidationError('Please use your UWE email address (@live.uwe.ac.uk)')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['study_program', 'study_year', 'bio', 'profile_picture', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address'}),
            'study_year': forms.Select(attrs={'class': 'form-select'}),
        }