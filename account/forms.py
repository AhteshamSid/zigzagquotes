from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.apps import apps


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'email-form', 'placeholder': 'Enter your Email'}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('quotes', 'Profile')
        fields = ('profile_pic', 'bio', 'date_of_birth', 'facebook_url', 'youtube_url', 'twitter_url', 'linkedin_url',
                  'instagram_url')
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy or yyyy/mm/dd'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paste url'}),
            'youtube_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paste url'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paste url'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paste url'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paste url'}),
        }
