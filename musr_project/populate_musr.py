import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musr_project.settings")

import django

django.setup()
from musr.models import Profile, Following, Post, User
from django.core.files.uploadedfile import SimpleUploadedFile


def populate():
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


def add_user(userName, firstName, lastName):
    u = User.objects.create_user(username=userName, password="password")
    u.email = "test@email.com"
    u.first_name = firstName
    u.last_name = lastName
    u.save()
    add_profile(u, firstName, lastName)
    return u


def add_profile(User, firstName, lastName):
    small_gif = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
        b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        b"\x02\x4c\x01\x00\x3b"
    )
    uploaded = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
    p = Profile.objects.get_or_create(user=User, picture=uploaded)
    return p


def add_following(follower, followee):
    f = Following.objects.create(follower=follower, followee=followee)
    return f


if __name__ == "__main__":
    populate()
