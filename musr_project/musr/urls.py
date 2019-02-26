from django.urls import path

from . import views

urlpatterns = [path("", views.test_page), path("account/", views.account)]
