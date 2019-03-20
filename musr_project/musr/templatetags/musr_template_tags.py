import urllib.request
import json

from django import template
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User
from musr.models import Profile, Post

register = template.Library()
# Used to highlight currently active page
@register.simple_tag(takes_context=True)
def current(context, url=None):
    if (
        "resolver_match" in context.request
        and context.request.resolver_match.url_name == url
    ):
        return "active"
    return ""


# Add post "component"
@register.inclusion_tag("musr/add_post.html")
def add_post():
    return {}


# Feed view "component"
@register.inclusion_tag("musr/songs.html")
def songs(posts, user, show_count=None):
    return {"posts": posts, "user": user, "show_count": show_count}


# Post "component"
@register.inclusion_tag("musr/song.html")
def song(post, user, show_count):
    if not post:
        raise SuspiciousOperation(
            "Invalid request; song can't be displayed without song id"
        )
        return

    poster = Profile.objects.get(user=post.poster)
    re_poster = None
    if post.original_poster:
        re_poster = poster
        poster = Profile.objects.get(user=post.original_poster)

    # Grab data from deezer
    url = "https://api.deezer.com/track/" + str(post.song_id)
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    data = json.loads(r.decode("utf-8"))

    if "error" in data:
        raise SuspiciousOperation("Invalid request; deezer song id is not a valid song")

    post.title = data["title"]
    post.artist = data["artist"]["name"]
    post.album = data["album"]["title"]
    post.album_art = data["album"]["cover_big"]
    post.preview = data["preview"]

    return {
        "song": post,
        "poster": poster,
        "re_poster": re_poster,
        "user": user,
        "show_count": show_count,
    }


# User List
@register.inclusion_tag("musr/user_list.html")
def user_list(users):
    return {"users": users}


@register.inclusion_tag("musr/user_list_item.html")
def user_list_item(user):
    profile = Profile.objects.get(user=user)
    return {"profile": profile}
