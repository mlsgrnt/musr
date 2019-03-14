from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.db import IntegrityError
from .models import Profile, Post, Following

# Index view (Whats hot)
def whats_hot(request):
    return render(request, "musr/whats_hot.html", {})


# Profile views (including redirect to own)
@login_required
def own_profile(request):
    return redirect("profile", username=request.user.username)


def profile(request, username):
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    own_profile = Profile.objects.get(user=request.user)

    profile = Profile.objects.get(user=user)
    profile_posts = Post.objects.filter(poster=profile)

    follower_count = profile.number_of_followers()

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
    profilesFollowed = Profile.objects.filter(follower__followee=profile)
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

    originalPost = Post.objects.get(post_id=request.POST["post"])

    profile = Profile.objects.get(user=request.user)

    song_id = originalPost.song_id

    newpost = Post.objects.create(
        poster=profile, original_poster=originalPost.poster, song_id=song_id
    )
    newpost.save()
    return HttpResponse("OK")


# Follow
@login_required
def follow(request):
    if request.method != "POST":
        return redirect("/")

    followee_username = request.POST["user"]

    followee_user = User.objects.get(username=followee_username)
    followee_profile = Profile.objects.get(user=followee_user)

    follower_user = request.user
    follower_profile = Profile.objects.get(user=follower_user)

    try:
        newFollowing = Following.objects.create(
            follower=follower_profile, followee=followee_profile
        )
        newFollowing.save()
        return HttpResponse("OK")
    except IntegrityError:
        return HttpResponseBadRequest()


# Delete post
@login_required
def delete_post(request):
    if request.method != "POST":
        return redirect("/")

    post_id = request.POST["post"]
    post = Post.objects.get(post_id=post_id)

    user = Profile.objects.get(user=request.user)
    poster = post.poster

    if user != poster:
        raise PermissionDenied

    post.delete()
    return HttpResponse("OK")


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
