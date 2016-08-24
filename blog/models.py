#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from smart_selects.db_fields import ChainedForeignKey


class Author(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __unicode__(self):
        return self.name + ' ' + self.last_name

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"


class Category(models.Model):
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"

DEFAULT_TOPIC =1
class SubCategory(models.Model):
    name = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, default=DEFAULT_TOPIC)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategoria"

DEFAULT_CATEGORY =1
DEFAULT_SUBCATEGORY =4
class Post(models.Model):
    CATEGORY_CHOICES= (('electronics', 'Electrónica'),
                 ('programming', 'Programación'))
    PROGRAMMING_CHOICES =(('python', 'Python'), )

    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created_at = models.DateTimeField(auto_now_add =True)
    published = models.BooleanField(default=True)
    body = RichTextUploadingField(default='')
    category = models.ForeignKey(Category, default=DEFAULT_CATEGORY )
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field = "category",
        chained_model_field ="category",
        show_all=False,
        auto_choose =True,
        default=DEFAULT_SUBCATEGORY
    )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:articulo_detalle', kwargs= { 'pk':self.id })

    class Meta:
        verbose_name = "Articulo"

class VisitCounter(models.Model):
    view_name = models.CharField(max_length=255)
    num_visits = models.IntegerField(default=0)

    def __unicode__(self):
        return "Visitas de " + self.view_name + '=' + str(self.num_visits)

    class Meta:
        verbose_name = "Contador de Visitas"
        verbose_name_plural = "Contadores de Visitas"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    title = models.CharField(max_length=120,default='', blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    body = models.TextField(blank=False,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __unicode__(self):
        return 'Comentario por {} {} para {}'.format(self.author.first_name, self.author.last_name, self.post )

