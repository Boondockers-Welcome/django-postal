from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^api/', include('postal.api.urls')),
    url(r'^update_postal_address/$', views.changed_country, name="changed_country"),
]