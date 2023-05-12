from django import forms
from newspost.models import NewsPostModel, CommentModel


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPostModel
        fields = ['title', 'photo', 'paragraph1', 'paragraph2', 'tag']
        labels = {'title':'', 'photo':'', 'paragraph1':'', 'paragraph2':'', 'tag':''}
        widgets = {
            'tag': forms.Select(attrs={'placeholder': 'Choose tag'}),
            'paragraph1': forms.Textarea(attrs={'cols': '110', 'rows': '12', 'class': 'formtext','style':"background-color: #ededed; font-size: 14px; padding-left: 10px;", 'placeholder': 'Write a paragraph'}),
            'title': forms.TextInput(attrs={'style':"background-color: #ededed; font-size: 36px; width: 350px; padding-left: 10px;", 'placeholder': 'Write a title'}),
        }