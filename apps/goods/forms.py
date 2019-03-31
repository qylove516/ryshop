# -*- coding: utf-8 -*-
# @Time    : 2019-03-27 10:49
# @Author  : Linxuan
# @Email   : yzlpython@163.com
from django import forms
from goods.models import Post, Images


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    body = forms.CharField(max_length=245, label="Item Description.")

    class Meta:
        model = Post
        fields = ('title', 'body',)


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)
