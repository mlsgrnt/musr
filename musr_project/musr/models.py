# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

# Profile Model
class Profile(models.Model):
    # link to django user model
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    # store user image
    picture = models.ImageField(upload_to="profile_images", blank=True)

    @property
    def post_count(self):
        return Post.objects.filter(poster=self).count

    @property
    def follower_count(self):
        followedBy = Following.objects.filter(followee=self)
        return followedBy.count()

    @property
    def picture_url(self):
        if self.picture:
            return self.picture.url
        else:
            return "/media/profile_images/default.jpg"

    def __str__(self):
        if self.user.first_name is not "":
            return self.user.first_name + " " + self.user.last_name

        return self.user.username


class Following(models.Model):
    # create two foreign keys from profile, one a follower and the other the followed
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower"
    )

    followee = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followee"
    )

    def clean(self):
        if self.followee == self.follower:
            raise ValidationError("User may not follow themselves.")

    # set the pair to function as a multi attribute primary key
    class Meta:
        unique_together = (("follower", "followee"),)
        verbose_name_plural = "following"


class Post(models.Model):
    # Automatically order most recent to least recent post
    class Meta:
        ordering = ("-date", "-post_id")

    # create a post ID as the post primary key
    post_id = models.AutoField(primary_key=True)

    # store Profile ID of poster
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="poster")

    # a foreign key field if the post is reposted
    original_poster = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="original_poster",
    )

    # a field for the song's Deezr ID
    song_id = models.IntegerField()

    # a field for the date the post was made
    date = models.DateField(default=timezone.now)
