from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
@login_required
def test_page(request):
    return render(request, "musr/test.html", {"user": request.user})
