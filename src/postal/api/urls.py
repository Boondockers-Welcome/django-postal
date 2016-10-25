from django.conf.urls import include, url
from ..resource import Resource
from postal.api.handlers import PostalHandler

postal_handler = Resource(PostalHandler)

urlpatterns = [
    url(r'^country/$', postal_handler, name="postal-api-country"),
]
