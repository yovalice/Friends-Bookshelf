from django import forms
from string import Template
from django.utils.safestring import mark_safe
from books.models import BooksRead

class UserPostForm(forms.Form):
    post = forms.CharField(
        required=True,
        label='Post',
        widget=forms.Textarea(attrs={'cols' : "80", 'rows': "4", 'placeholder': 'Post about yourself or books.'})
    )
    book_choice = forms.ModelChoiceField(
        queryset=None,
        label="Book Reads Recommendation",
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        super(UserPostForm, self).__init__(*args, **kwargs)
        self.fields['book_choice'].queryset = BooksRead.objects.select_related('book').filter(
            user=user).order_by('-created_date')
    
    
