from django import forms
from django.forms import ModelForm
from article.models import Article, Comment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']