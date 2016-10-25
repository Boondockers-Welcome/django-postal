import os

from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^admin/(.*)', include(admin.site.urls)),
    url(r'^postal/', include('postal.urls')),
    url(r'^site_media/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.DIRNAME, "media"), 'show_indexes': True }),
    url(r'^$', views.test_postal, name="postal-home"),
    url(r'^json$', views.test_postal_json, name="postal-home"),
]
