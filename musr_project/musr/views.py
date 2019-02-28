from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

# Index view (Whats hot)
def whats_hot(request):
    return render(request, "musr/whats_hot.html", {"user": request.user})


# Profile
@login_required
def profile(request):
    return render(request, "musr/profile.html", {"user": request.user})


@login_required
def feed(request):
    return render(request, "musr/feed.html", {"user": request.user})
