from django.conf import settings
from django.conf.urls import url, include, patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from . import views
from django.contrib.auth.views import  (login,
                                        logout,
                                        logout_then_login,
                                        password_change,
                                        password_change_done,
                                        password_reset,
                                        password_reset_done,
                                        password_reset_confirm,
                                        password_reset_complete
                                        )
from blog.views import register, home_view

urlpatterns = [
    # url(r'^$', views.home_view, name='home'),
    url(r'^$', home_view, name='home'),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^login/$',login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^logout_then_login/$', logout_then_login, name='logout_then_login'),
    url(r'^password_change/$', password_change, name='password_change'),
    url(r'^password_change/done/$', password_change_done, name='password_change_done'),
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset_done/$', password_reset_done, name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^password_reset_complete', password_reset_complete, name='password_reset_complete'),
    url(r'^register/$', register, name='register'),
    url(r'^mywiki/', include('mywiki.urls', namespace='mywiki', app_name='mywiki')),
    url('social-auth/', include('social.apps.django_app.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

