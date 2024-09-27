from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts
        for field in self.fields.values():
            field.help_text = None

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        return cleaned_data



class UploadForm(forms.Form):
    file = forms.FileField(label='Upload a file with expressions', required=True)  # required=True is default

