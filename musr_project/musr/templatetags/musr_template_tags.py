from django import template

from django.contrib.auth.models import User
from musr.models import Profile

register = template.Library()


# Used to highlight currently active page
@register.simple_tag(takes_context=True)
def current(context, url=None):
    if context.request.resolver_match.url_name == url:
        return "active"
    return ""


# Post "component"
@register.inclusion_tag("musr/song.html")
def song(post):
    # TODO: fail on no post --> unit test
    # TODO: make this more elegant
    poster = Profile.objects.get(user=post.poster)
    re_poster = None  # TODO IS THIS PYTHON STYLE
    if post.original_poster:
        re_poster = poster
        poster = Profile.objects.get(user=post.original_poster)

    return {"post": post, "poster": poster, "re_poster": re_poster}
