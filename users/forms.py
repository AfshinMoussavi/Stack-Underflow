from django import forms
from django.core.exceptions import ValidationError
from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'phone_number' , 'national_id']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise ValidationError("This email is already exist!")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and username != self.instance.username:
            raise ValidationError("This username is already exist!")
        return username



class UserRegisterForm(UserUpdateForm):
    confirm_password = forms.CharField(label="confirm_password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields  = ['username' , 'email' , 'phone_number' , 'password' , 'national_id']
        widgets = {
            'password' : forms.PasswordInput
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if not password or not confirm_password:
            raise forms.ValidationError('Enter the both of password')
        
        if password != confirm_password:
            raise forms.ValidationError("Password must match")
        
        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(label = 'username' , max_length=80)
    password = forms.CharField(label = 'password' , widget=forms.PasswordInput())

