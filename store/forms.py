from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Wprowadź nazwę użytkownika', 'id': 'login'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Wprowadź hasło',
            'id': 'password',
        }
))

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Wprowadź nazwę użytkownika',
            'id': 'username',
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Wprowadź imię',
            'id': 'first_name',
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Wprowadź nazwisko',
            'id': 'last_name',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Wprowadź e-mail',
            'id': 'email',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Wprowadź hasło',
            'id': 'password1',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Potwierdź hasło',
            'id': 'password2',
        })

    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)    
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']  

# class UserRegisterForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserRegisterForm, self).__init__(*args, **kwargs)

#     username = UsernameField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Wprowadź nazwę użytkownika', 'id': 'login'}))
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Wprowadź E-mail', 'id': 'email'}))

#     password1 = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Wprowadź hasło',
#             'id': 'password1',
#         }))
#     password2 = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': 'Potwierdź hasło',
#             'id': 'password2',
#         }))  