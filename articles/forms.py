from django import forms
from django.forms import ModelForm
from .models import Comment
from crispy_forms.helper import FormHelper


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField(label="")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

