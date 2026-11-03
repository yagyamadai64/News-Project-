from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from news_app.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ("author", "view_count", "published_at")


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
