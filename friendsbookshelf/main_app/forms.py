from django import forms
from string import Template
from django.utils.safestring import mark_safe


class UserPostForm(forms.Form):
    post = forms.CharField(
        required=True,
        label='Post',
        widget=forms.Textarea(attrs={'cols' : "80", 'rows': "3", })
    )
    
