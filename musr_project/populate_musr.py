import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musr_project.settings")

import django
import datetime

django.setup()
from django.contrib.sites.models import Site
from musr.models import Profile, Following, Post, User
from django.core.files.uploadedfile import SimpleUploadedFile


def populate():
    setUpAllAuth()

    musers = [
        {"user": "Drake", "firstName": "Drake", "lastName": "Graham"},
        {"user": "Beethoven", "firstName": "Ludwig", "lastName": "Beethoven"},
        {"user": "PeterParker", "firstName": "Peter", "lastName": "Parker"},
        {"user": "MichaelScott", "firstName": "Michael", "lastName": "Scott"},
        {"user": "PostMalone", "firstName": "Austin", "lastName": "Malone"},
        {"user": "FreddieMercury", "firstName": "Freddie", "lastName": "Mercury"},
    ]

    followers = [
        {"follower": "Drake", "followee": "Beethoven"},
        {"follower": "Drake", "followee": "PeterParker"},
        {"follower": "PeterParker", "followee": "Drake"},
        {"follower": "PostMalone", "followee": "Beethoven"},
        {"follower": "Beethoven", "followee": "FreddieMercury"},
        {"follower": "Drake", "followee": "FreddieMercury"},
        {"follower": "PostMalone", "followee": "MichaelScott"},
        {"follower": "Drake", "followee": "MichaelScott"},
    ]

    posts = [
        {"poster": "Drake", "original": "Drake", "Song_Id": 639437722},
        {"poster": "Ludwig", "original": "Drake", "Song_Id": 639437722},
        {"poster": "PostMalone", "original": "Drake", "Song_Id": 639437722},
        {"poster": "MichaelScott", "original": "Drake", "Song_Id": 639437722},
        {"poster": "PeterParker", "original": "Drake", "Song_Id": 639437722},
        {"poster": "FreddieMercury", "original": "Drake", "Song_Id": 639437722},
        {"poster": "Ludwig", "original": "Ludwig", "Song_Id": 5707517},
        {"poster": "Drake", "original": "Ludwig", "Song_Id": 5707517},
        {"poster": "PostMalone", "original": "PostMalone", "Song_Id": 3135556},
        {"poster": "PeterParker", "original": "PostMalone", "Song_Id": 3135556},
    ]

    x = 0
    for users in musers:
        value = musers[x]
        x = x + 1
        add_user(value["user"], value["firstName"], value["lastName"])

    y = 0
    for users in followers:
        value = followers[y]
        add_following(
            Profile.objects.get(user=User.objects.get(username=value["follower"])),
            Profile.objects.get(user=User.objects.get(username=value["followee"])),
        )
        y = y + 1
    z = 0
    for post in posts:
        value = posts[z]
        add_post(value["poster"], value["original"], value["Song_Id"])


def add_user(userName, firstName, lastName):
    u, was_created = User.objects.get_or_create(
        username=userName, password="password", email="test@email.com"
    )
    u.first_name = firstName
    u.last_name = lastName
    u.save()
    # add_profile(u, firstName, lastName)
    return u


def add_profile(User, firstName, lastName):
    small_gif = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
        b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        b"\x02\x4c\x01\x00\x3b"
    )
    uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
    p = Profile.objects.get(user=User)
    p.picture = uploaded
    p.save()
    return p


def add_following(follower, followee):
    f = Following.objects.create(follower=follower, followee=followee)
    return f


def add_post(posterParam, original_posterParam, Song_IdParam):
    po = Post.objects.create(
        poster=Profile.objects.get(user=User.objects.get(username=posterParam)),
        original_poster=Profile.objects.get(
            user=User.objects.get(username=original_posterParam)
        ),
        song_id=Song_IdParam,
        date=datetime.datetime.now(),
    )
    return po


def setUpAllAuth():
    current_site = Site.objects.get_current()
    current_site.socialapp_set.create(
        provider="facebook",
        name="facebook",
        client_id="1234567890",
        secret="0987654321",
    )
    current_site.socialapp_set.create(
        provider="google", name="google", client_id="1234567890", secret="0987654321"
    )


if __name__ == "__main__":
    populate()
