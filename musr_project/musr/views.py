from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.db.models import Q
from django.template import loader, Context
from django.db import IntegrityError
from django.utils import timezone
from .models import Profile, Post, Following
from math import log10
from datetime import timedelta


# Index view (Whats hot)
def whats_hot(request):
    # Get all posts made within the last month
    current_time = timezone.now()
    four_weeks_ago = current_time - timedelta(days=28)
    all_posts = Post.objects.filter(date__gte=four_weeks_ago).order_by("date")

    song_ids = []

    for post in all_posts:
        if post.song_id not in song_ids:
            song_ids.append(post.song_id)

    # Get all original posts made within the last month
    song_rankings = {song_id: 1 for song_id in song_ids}

    # Increase rankings each time we find a duplicate
    for post in all_posts:
        if post.song_id in song_rankings:
            song_rankings[post.song_id] += 1

    # Decay the longer ago a post was reposted
    for song_id in song_rankings.keys():
        days_since_posting = (current_time.date() - post.date).days
        song_rankings[song_id] = song_rankings[song_id] / log10(
            (4 + days_since_posting) / 3.2
        )

    sorted_songs = sorted(song_rankings.items(), key=lambda x: x[1], reverse=True)
    sorted_posts = []

    for song in sorted_songs:
        sorted_posts.append(
            Post.objects.filter(date__gte=four_weeks_ago, song_id=song[0]).order_by(
                "date"
            )[0]
        )

    return render(request, "musr/whats_hot.html", {"posts": sorted_posts[:6]})


# Profile views (including redirect to own)
@login_required
def own_profile(request):
    return redirect("profile", username=request.user.username)


def profile(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    profile = Profile.objects.get(user=user)
    profile_posts = Post.objects.filter(poster=profile)

    follower_count = profile.number_of_followers()

    follow_button_text = ""
    if request.user.is_authenticated:
        own_profile = Profile.objects.get(user=request.user)
        follow_button_text = (
            "Unfollow"
            if Following.objects.filter(follower=own_profile, followee=profile).exists()
            else "Follow"
        )

    return render(
        request,
        "musr/profile.html",
        {
            "profile": profile,
            "posts": profile_posts,
            "follower_count": follower_count,
            "post_count": profile_posts.count,
            "posting_since": profile.user.date_joined,
            "follow_button_text": follow_button_text,
        },
    )


# Account info
@login_required
def account(request):
    return render(request, "musr/account.html")


# Feed view
@login_required
def feed(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profilesFollowed = Profile.objects.filter(followee__follower=profile)
    posts = Post.objects.filter(poster__in=profilesFollowed)
    return render(request, "musr/feed.html", {"posts": posts})


# Add post!
@login_required
def add_post(request):
    if request.method != "POST":
        return redirect("/")

    # TODO: validate this data!!!! this is begging for mysql injection
    song_id = request.POST["song"]
    profile = Profile.objects.get(user=request.user)

    newpost = Post.objects.create(poster=profile, song_id=song_id)

    return HttpResponse("OK")


# repost
@login_required
def repost(request):
    if request.method != "POST":
        return redirect("/")

    original_post = Post.objects.get(post_id=request.POST["post_id"])

    profile = Profile.objects.get(user=request.user)

    song_id = original_post.song_id

    newpost = Post.objects.create(
        poster=profile, original_poster=original_post.poster, song_id=song_id
    )
    newpost.save()
    return HttpResponse("OK")


# Follow
@login_required
def follow(request):
    if request.method != "POST":
        return redirect("/")

    followee_username = request.POST["username"]

    followee_user = User.objects.get(username=followee_username)
    followee_profile = Profile.objects.get(user=followee_user)

    follower_user = request.user
    follower_profile = Profile.objects.get(user=follower_user)

    try:
        new_following = Following.objects.create(
            follower=follower_profile, followee=followee_profile
        )

        new_following.clean()
        new_following.save()

        return HttpResponse("OK")
    except:
        return HttpResponseBadRequest()


# Unfollow
@login_required
def unfollow(request):
    if request.method != "POST":
        return redirect("/")

    unfollow_username = request.POST["username"]

    unfollow_user = User.objects.get(username=unfollow_username)
    unfollow_profile = Profile.objects.get(user=unfollow_user)

    profile = Profile.objects.get(user=request.user)
    try:
        following = Following.objects.get(follower=profile, followee=unfollow_profile)

        following.delete()
        return HttpResponse("OK")
    except:
        return HttpResponseBadRequest()


# Delete post
@login_required
def delete_post(request):
    if request.method != "POST":
        return redirect("/")

    post_id = request.POST["post_id"]
    post = Post.objects.get(post_id=post_id)

    user = Profile.objects.get(user=request.user)
    poster = post.poster

    if user != poster:
        raise PermissionDenied

    post.delete()
    return HttpResponse("OK")


# Change first or last name
@login_required
def change_name(request):
    if request.method != "POST":
        redirect("/")
    user = request.user

    if (
        request.POST["name_to_change"] != "first_name"
        and request.POST["name_to_change"] != "last_name"
    ):
        raise PermissionDenied

    try:

        setattr(user, request.POST["name_to_change"], request.POST["new_name"])
        user.save()
        return HttpResponse("OK")
    except:
        return HttpResponseBadRequest()


# Account photo upload
@login_required
def photo_upload(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        if profile and "photoUpload" in request.FILES:
            if (
                request.FILES["photoUpload"].name.lower().endswith(".jpg")
                and request.FILES["photoUpload"].size < 512000
            ):
                profile.picture = request.FILES["photoUpload"]
                profile.save()
            else:
                return HttpResponse(
                    "You can only upload .jpg files smaller than 512KB as a profile picture"
                )

    return render(request, "musr/photo_upload.html", {"profile": profile})


def search(request):
    search = request.POST["query"]
    us = User.objects.filter(
        Q(username__contains=search)
        | Q(first_name__contains=search)
        | Q(last_name__contains=search)
    )

    return render(
        request, "musr/search_account.html", {"query": us, "search": search.lower()}
    )
