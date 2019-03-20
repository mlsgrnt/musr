from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path("", views.whats_hot, name="whats_hot"),
    path("account/", views.account, name="account"),
    path("feed/", views.feed, name="feed"),
    path("profile/", views.own_profile, name="own_profile"),
    path("profile/<slug:username>/", views.profile, name="profile"),
    path(
        "profile/<slug:username>/followers", views.get_followers, name="get_followers"
    ),
    path(
        "profile/<slug:username>/following", views.get_followees, name="get_followees"
    ),
    path("search", views.search, name="search"),
    path("add-post", views.add_post, name="add_post"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("repost-post", views.repost, name="repost_post"),
    path("delete-post", views.delete_post, name="delete_post"),
]
