from django import forms
from .models import User, Article, Image

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file']

class ImageProcessForm(forms.Form):
    width = forms.IntegerField()
    height = forms.IntegerField()
    left = forms.IntegerField()
    top = forms.IntegerField()
    right = forms.IntegerField()
    bottom = forms.IntegerField()