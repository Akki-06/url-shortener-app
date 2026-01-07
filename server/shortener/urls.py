from django.urls import path
from .views import *

urlpatterns = [
    path("api/shorten/",shorten_url),
     path("<str:short_code>/", redirect_url),
]
