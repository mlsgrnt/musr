from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.whats_hot, name="whats_hot"),
    path("feed/", views.feed, name="feed"),
    # TODO:
    # How to match to profile/username/
    path("profile/", views.profile, name="profile"),
]
