from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Index view (Whats hot)
def whats_hot(request):
    return render(request, "musr/whats_hot.html", {"user": request.user})


# Does profile require login?
@login_required
def profile(request):
    return render(request, "musr/profile.html", {"user": request.user})


# Feed view
@login_required
def feed(request):
    return render(request, "musr/feed.html", {"user": request.user})
