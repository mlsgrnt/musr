import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "musr_project.settings")

import django
import datetime
import base64
import binascii
import functools
import hashlib
import importlib
import warnings

django.setup()
from django.contrib.sites.models import Site
from musr.models import Profile, Following, Post, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.crypto import constant_time_compare, get_random_string, pbkdf2


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
        {"poster": "Beethoven", "original": "Drake", "Song_Id": 639437722},
        {"poster": "PostMalone", "original": "Drake", "Song_Id": 639437722},
        {"poster": "MichaelScott", "original": "Drake", "Song_Id": 639437722},
        {"poster": "PeterParker", "original": "Drake", "Song_Id": 639437722},
        {"poster": "FreddieMercury", "original": "Drake", "Song_Id": 639437722},
        {"poster": "Beethoven", "original": "Beethoven", "Song_Id": 5707517},
        {"poster": "Drake", "original": "Beethoven", "Song_Id": 5707517},
        {"poster": "PostMalone", "original": "PostMalone", "Song_Id": 3135556},
        {"poster": "PeterParker", "original": "PostMalone", "Song_Id": 3135556},
    ]

    for user in musers:
        value = user
        add_user(value["user"], value["firstName"], value["lastName"])

    for user in followers:
        value = user
        add_following(
            Profile.objects.get(user=User.objects.get(username=value["follower"])),
            Profile.objects.get(user=User.objects.get(username=value["followee"])),
        )
    for post in posts:
        value = post
        add_post(value["poster"], value["original"], value["Song_Id"])


def add_user(userName, firstName, lastName):
    u, was_created = User.objects.get_or_create(
        username=userName,
        password=make_password("testpassword123"),
        email="test@email.com",
    )
    u.first_name = firstName
    u.last_name = lastName
    u.save()
    add_profile(u)
    return u


def add_profile(User):
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


# https://docs.djangoproject.com/en/2.1/_modules/django/contrib/auth/hashers/
@functools.lru_cache()
def get_hashers():
    hashers = []
    for hasher_path in settings.PASSWORD_HASHERS:
        hasher_cls = import_string(hasher_path)
        hasher = hasher_cls()
        if not getattr(hasher, "algorithm"):
            raise ImproperlyConfigured(
                "hasher doesn't specify an " "algorithm name: %s" % hasher_path
            )
        hashers.append(hasher)
    return hashers


@functools.lru_cache()
def get_hashers_by_algorithm():
    return {hasher.algorithm: hasher for hasher in get_hashers()}


def get_hasher(algorithm="default"):
    """
    Return an instance of a loaded password hasher.

    If algorithm is 'default', return the default hasher. Lazily import hashers
    specified in the project's settings file if needed.
    """
    if hasattr(algorithm, "algorithm"):
        return algorithm

    elif algorithm == "default":
        return get_hashers()[0]

    else:
        hashers = get_hashers_by_algorithm()
        try:
            return hashers[algorithm]
        except KeyError:
            raise ValueError(
                "Unknown password hashing algorithm '%s'. "
                "Did you specify it in the PASSWORD_HASHERS "
                "setting?" % algorithm
            )


def make_password(password, salt=None, hasher="default"):
    """
    Turn a plain-text password into a hash for database storage

    Same as encode() but generate a new random salt. If password is None then
    return a concatenation of UNUSABLE_PASSWORD_PREFIX and a random string,
    which disallows logins. Additional random string reduces chances of gaining
    access to staff or superuser accounts. See ticket #20079 for more info.
    """
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(
            UNUSABLE_PASSWORD_SUFFIX_LENGTH
        )
    hasher = get_hasher(hasher)
    salt = salt or hasher.salt()
    return hasher.encode(password, salt)


if __name__ == "__main__":
    populate()
