# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from . import models

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don\'t match.")
        return cd['password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title',
                  'published',
                  'body',
                  'category',
                  'subcategory'
                  ]
        labels = { 'title': 'Título',
                   'published': 'Públicado',
                   'body': 'Contenido',
                   'category': 'Categoría',
                   'subcategory': 'Subcategoría'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = [ 'title',
                  'body']
        labels = { 'title':u'Título',
                    'body': 'Mensaje'}
