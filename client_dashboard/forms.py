from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}),

        }


class DeactivateAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input'})
        }
