from django import forms
from .models import Comment


class SearchForm(forms.Form):
    query = forms.CharField(max_length=30, )


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", 'email', 'body')
        widgets = {'name': forms.TextInput(
            attrs={'placeholder': "Enter you name here"}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email here.'}),
            'body': forms.Textarea(attrs={"placeholder": "Enter your feedback  here"})

        }
