# forms.py
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    # important exact name
    first_name = forms.CharField(max_length=150, required=True)

    last_name = forms.CharField(max_length=150, required=True)

    password = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    con_password = forms.CharField(widget=forms.PasswordInput(), min_length=8)

    class Meta:
        model = User
        # These are the fields Django checks during form.is_valid()
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        con_password = cleaned_data.get("con_password")

        if password and con_password and password != con_password:
            self.add_error('con_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username identical to email behind the scenes
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
