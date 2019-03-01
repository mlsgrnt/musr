from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect


# Index view (Whats hot)
def whats_hot(request):
    return render(request, "musr/whats_hot.html", {})


@login_required
def own_profile(request):
    return redirect("profile", username=request.user.username)


def profile(request, username):
    return render(request, "musr/profile.html", {"username": username})


# Feed view
@login_required
def feed(request):
    return render(request, "musr/feed.html", {})
