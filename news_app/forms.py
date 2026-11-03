from django import forms
from news_app.models import Contact, Comment, NewsLetters


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetters
        fields = "__all__"
