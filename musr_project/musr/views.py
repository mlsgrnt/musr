from django.shortcuts import render, redirect, reverse
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
from django.contrib import messages


# User-visitable views
# Index view (Whats hot)
def whats_hot(request):
    # Get all posts made within the last month
    current_time = timezone.now()
    four_weeks_ago = current_time - timedelta(days=28)
    all_posts = Post.objects.filter(date__gte=four_weeks_ago).order_by("date")

    song_ids = []

    # Populate list of all song ids
    for post in all_posts:
        if post.song_id not in song_ids:
            song_ids.append(post.song_id)

    # Give each song a starting ranking of 1
    song_rankings = {song_id: 1 for song_id in song_ids}

    # Increase rankings each time we find a duplicate
    for post in all_posts:
        if post.song_id in song_rankings:
            song_rankings[post.song_id] += 1

    # Decrease ranking based on how long ago each song was posted
    for post in all_posts:
        song_id = post.song_id

        days_since_posting = (current_time.date() - post.date).days
        song_rankings[song_id] = song_rankings[song_id] / log10(
            (4 + days_since_posting) / 3.2
        )

    # Sort all songs by their rank
    sorted_songs = sorted(song_rankings.items(), key=lambda x: x[1], reverse=True)
    sorted_posts = []

    # Find oldest post for each song, which will then be shown
    for song in sorted_songs:
        sorted_posts.append(
            Post.objects.filter(date__gte=four_weeks_ago, song_id=song[0]).order_by(
                "date"
            )[0]
        )

    # Show only the top 6 posts
    return render(request, "musr/whats_hot.html", {"posts": sorted_posts[:6]})


# Profile views (including redirect to own)

# A view which redirects to the profile of the current user
@login_required
def own_profile(request):
    return redirect("profile", username=request.user.username)


# View which shows a user's profile
def profile(request, username):
    # Get user from username
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    # Get profile from user
    profile = Profile.objects.get(user=user)

    # Get posts from profile
    profile_posts = Post.objects.filter(poster=profile)

    # Determine the relationship between the currently logged in user
    # and the profile of the given user
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
            "follow_button_text": follow_button_text,
        },
    )


# View which displays all followers of a user
def get_followers(request, username):
    # Get user object from username
    try:
        user = User.objects.select_related("profile").get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    # Get profile object from user object
    profile = user.profile

    # Get list of followers
    followers = Following.objects.filter(followee=profile)

    # Convert from queryset to list
    followers_list = [i.follower for i in followers]

    return render(
        request, "musr/followers.html", {"list": followers_list, "request_user": user}
    )


# View which displays all followees of a user
def get_followees(request, username):
    # Get user object from username
    try:
        user = User.objects.select_related("profile").get(username__iexact=username)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    # Get profile object from user object
    profile = user.profile

    # Get set of users which user is following
    followees = Following.objects.filter(follower=profile)

    # Convert to python list
    followees_list = [i.followee for i in followees]

    return render(
        request, "musr/following.html", {"list": followees_list, "request_user": user}
    )


# View which renders the main account page
@login_required
def account(request):
    return render(request, "musr/account.html")


# View which shows the feed of the logged in user
# This is all the posts made my all the users the user is following
@login_required
def feed(request):
    user = request.user

    # Get profile from user
    profile = Profile.objects.get(user=user)

    # Get list of profiles followed
    profilesFollowed = Profile.objects.filter(followee__follower=profile)

    # Get relevant posts
    posts = Post.objects.filter(poster__in=profilesFollowed)

    # Potential scalability issue: as users post more and more posts
    # simply returning the entire post list can lead to a very slow loading page
    return render(request, "musr/feed.html", {"posts": posts})


# Views with forms:

# View which allows users to change their first and last name
@login_required
def change_name(request):
    user = request.user

    if request.method == "POST":
        try:
            fname = request.POST.get("firstName")
            lname = request.POST.get("lastName")
        except:
            return HttpResponseBadRequest()

        # Check if the name should be cleared
        if not fname:
            lname = ""

        # Check length constraint
        if (fname and len(fname) > 20) or (lname and len(lname) > 20):
            messages.error(
                request,
                "Your name can not be empty or greater than 20 alphabetical letters!",
            )
        else:
            # Captialize names
            user.first_name = fname.capitalize()
            user.last_name = lname.capitalize()

            # Save update user
            user.save()

            # Get profile to print out new name
            profile = Profile.objects.get(user=user)
            if fname == "":
                messages.success(
                    request,
                    "Name removed successfully! You are now " + str(profile) + "!",
                )
            else:
                messages.success(
                    request,
                    "Name changed successfully! You are now " + str(profile) + "!",
                )

    return render(request, "account/change_name.html")


# View which allows users to upload or remove their profile picture
@login_required
def photo_upload(request):
    user = request.user
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        # New photo has been passed for upload
        if "photoUpload" in request.FILES:
            # Verify contraints
            if (
                request.FILES["photoUpload"].name.lower().endswith(".jpg")
                or request.FILES["photoUpload"].name.lower().endswith(".png")
                or request.FILES["photoUpload"].name.lower().endswith(".gif")
                and request.FILES["photoUpload"].size < 4096000
            ):
                # Update profile
                profile.picture = request.FILES["photoUpload"]
                profile.save()

                messages.success(
                    request, "Your profile picture has uploaded successfully!"
                )
            else:
                messages.error(
                    request,
                    "You can only upload .jpg, .png or .gif files smaller than 4MB as a profile picture!",
                )
        # Photo remove button has been clicked, no new photo available for upload
        elif "photoRemove" in request.POST and request.POST["photoRemove"] == "true":
            # Update profile
            profile.picture = None
            profile.save()

            messages.success(request, "Photo removed successfully!")
        # Invalid form passed
        else:
            messages.error(request, "You must select a photo to upload!")

    return render(request, "account/photo_upload.html", {"profile": profile})


# View which shows search results for a given query
def search(request):
    if request.method == "POST":
        try:
            search = request.POST["query"]
        except:
            return HttpResponseBadRequest()

        # Execute the search
        us = User.objects.filter(
            Q(username__icontains=search)
            | Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
        )

        # Execute search again on each word of the search
        search_words = search.split()
        for word in search_words:
            # Concatenate search results
            us = us | User.objects.filter(
                Q(username__icontains=word)
                | Q(first_name__icontains=word)
                | Q(last_name__icontains=word)
            )

        return render(
            request, "musr/search_account.html", {"query": us, "search": search.lower()}
        )
    # If someone tried to visit the page directly, fail
    else:
        return redirect(reverse("whats_hot"))


# API endpoint views which are not to be visited directly, but rather through requests crafted via javascript
# These all have fairly generic exceptions as they (should) only be called by crafed requests
# Therefore the error can be handled client side

# Endpoint which creates a new post
@login_required
def add_post(request):
    if request.method != "POST":
        return redirect(reverse("whats_hot"))

    try:
        song_id = request.POST["song"]
    except:
        return HttpResponseBadRequest()

    # Check song_id is valid
    try:
        int(song_id)
    except ValueError:
        return HttpResponseBadRequest()

    # Get profile from user
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        return HttpResponseBadRequest()

    # If something goes wrong in this process, the method will create an exception which will cause the method
    # to fail, and OK not to be returned
    Post.objects.create(poster=profile, song_id=song_id)

    return HttpResponse("OK")


# Endpoint which creates a repost
@login_required
def repost(request):
    if request.method != "POST":
        return redirect(reverse("whats_hot"))

    try:
        # Get original post from post_id
        original_post = Post.objects.get(post_id=request.POST["post_id"])

        # Get profile of currently logged in user
        profile = Profile.objects.get(user=request.user)
    except:
        return HttpResponseBadRequest()

    newpost = Post.objects.create(
        poster=profile,
        original_poster=original_post.poster,
        song_id=original_post.song_id,
    )
    newpost.save()

    return HttpResponse("OK")


# Endpoint which will cause the current user to follow another
@login_required
def follow(request):
    if request.method != "POST":
        return redirect(reverse("whats_hot"))

    try:
        followee_username = request.POST["username"]

        # Get profile of user to follow
        followee_user = User.objects.get(username=followee_username)
        followee_profile = Profile.objects.get(user=followee_user)

        # Get profile of currently logged in user
        follower_user = request.user
        follower_profile = Profile.objects.get(user=follower_user)

        # Create new following object
        new_following = Following.objects.create(
            follower=follower_profile, followee=followee_profile
        )

        # Verify that this following is legitimate (unique, and not a user following themselves)
        new_following.clean()
        new_following.save()
    except:
        return HttpResponseBadRequest()

    return HttpResponse("OK")


# Endpoint which will cause the current user to unfollow another
@login_required
def unfollow(request):
    if request.method != "POST":
        return redirect(reverse("whats_hot"))

    try:
        unfollow_username = request.POST["username"]

        # Get profile of user to unfollow
        unfollow_user = User.objects.get(username=unfollow_username)
        unfollow_profile = Profile.objects.get(user=unfollow_user)

        # Get profile of currently logged in user
        profile = Profile.objects.get(user=request.user)

        # Find and delete relevant following object
        following = Following.objects.get(follower=profile, followee=unfollow_profile)
        following.delete()

    except:
        return HttpResponseBadRequest()

    return HttpResponse("OK")


# Endpoint which will delete a specified post of a user
@login_required
def delete_post(request):
    if request.method != "POST":
        return redirect(reverse("whats_hot"))

    try:
        # Get post from passed post_id
        post_id = request.POST["post_id"]
        post = Post.objects.get(post_id=post_id)

        # Get relevant users for our operation
        user = Profile.objects.get(user=request.user)
        poster = post.poster
    except:
        return HttpResponseBadRequest()

    if user != poster:
        raise PermissionDenied

    # Actually delete the post
    post.delete()

    return HttpResponse("OK")
