from django import forms
from string import Template
from django.utils.safestring import mark_safe

class UserLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=100
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=255,
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
        max_length=100
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        max_length=100,
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=255,
        widget=forms.PasswordInput()
    )


class UserForgotForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label='Email Address',
        max_length=100,
    )


class UserConfirmationPasswordForm(forms.Form):
    password1 = forms.CharField(
        required=True,
        label='Password',
        max_length=255,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        required=True,
        label='Confirm Password',
        max_length=255,
        widget=forms.PasswordInput()
    )


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class UserInformationForm(forms.Form):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
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
    bio = forms.CharField(
        required=True,
        label='User Bio',
        widget=forms.Textarea(attrs={'cols' : "80", 'rows': "4", })
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    image = forms.ImageField()
