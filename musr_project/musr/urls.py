from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("", views.whats_hot, name="whats_hot"),
    path("feed/", views.feed, name="feed"),
    path("profile/", views.own_profile, name="own_profile"),
    path("profile/<slug:username>/", views.profile, name="profile"),
    path("add-post", views.add_post, name="add_post"),
]
