#!/usr/bin/emv python
# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

from . import views

urlpatterns = [
    url(r'^/', views.home_view, name="home"),
    url(r'^get_comments/(?P<pk>\d+)/', views.ajax_send_comments, name='get_comments'),
    url(r'^articulo_detalle/(?P<pk>\d+)/', views.detail_view, name='articulo_detalle'),
    url(r'^article_list/(?P<category_pk>\d+)/(?P<subcategory_pk>\d+)/',
        views.article_list, name ="article_list_category_subcategory"),
    url(r'^article_list/(?P<category_pk>\d+)/', views.article_list, name ="article_list_category"),
    url(r'^article_list/', views.article_list, name ="article_list"),
    url(r'^create_post/', views.create_post, name="create_post"),
    url(r'^edit_post/(?P<pk>\d+)/', views.edit_post, name="edit_post"),
    url(r'^list_user_posts$', views.list_user_posts, name='list_user_posts'),
    url(r'^$', views.dashboard, name='dashboard')
]