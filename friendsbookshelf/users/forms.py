from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )

class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        label='First Name',
        max_length=32
    )
    last_name = forms.CharField(
        required=True,
        label='Last Name',
        max_length=32
    )
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )


class UserForgotForm(forms.Form):
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
    )

