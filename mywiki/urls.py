from django.conf.urls import url, patterns

from mywiki import views

urlpatterns = [
    url(r'^/', views.home_view, name='wiki_home'),
]
