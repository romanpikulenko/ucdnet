from django import forms
from django.contrib.auth.password_validation import validate_password


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=254, required=True, widget=forms.PasswordInput, validators=[validate_password]
    )
    password_confirm = forms.CharField(max_length=254, required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
