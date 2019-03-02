from django.test import TestCase
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile, Post, Following

# Create your tests here.
class TravisTesterTestCase(TestCase):
    def test_unit_tests_are_understood_and_can_pass(self):
        """Unit tests run and are able to pass"""
        test_value = 5
        self.assertEqual(test_value, 5)

class ModelTestCase(TestCase):
    def test_can_create_user(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        self.assertTrue(isinstance(self.user, User))

    def test_can_create_profile(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user)

        self.assertTrue(isinstance(self.profile, Profile))

    def test_user_deletion_cascades(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user.save()

        self.profile = Profile.objects.create(user=self.user)
        self.profile.save()

        self.user.delete()

        self.assertQuerysetEqual(Profile.objects.all(), [])

    def test_can_create_following_relationship(self):
        self.follower = User.objects.create_user(
            username="testuser", password="password"
        )
        self.follower.save()

        self.follower_profile = Profile.objects.create(user=self.follower)
        self.follower_profile.save()

        self.followee = User.objects.create_user(
            username="testuser2", password="password"
        )
        self.followee.save()

        self.followee_profile = Profile.objects.create(user=self.followee)
        self.followee_profile.save()

        self.following = Following.objects.create(
            follower=self.follower_profile, followee=self.followee_profile
        )
        self.following.save()

        self.assertTrue(isinstance(self.following, Following))

    def test_user_deletion_cascades_following(self):
        self.follower = User.objects.create_user(
            username="testuser", password="password"
        )
        self.follower.save()

        self.follower_profile = Profile.objects.create(user=self.follower)
        self.follower_profile.save()

        self.followee = User.objects.create_user(
            username="testuser2", password="password"
        )
        self.followee.save()

        self.followee_profile = Profile.objects.create(user=self.followee)
        self.followee_profile.save()

        self.following = Following.objects.create(
            follower=self.follower_profile, followee=self.followee_profile
        )
        self.following.save()

        self.follower.delete()

        self.assertQuerysetEqual(Following.objects.all(), [])

# TODO: refactor these
class baseLinksTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.current_site = Site.objects.get_current()
        self.SocialApp1 = self.current_site.socialapp_set.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )
        self.SocialApp2 = self.current_site.socialapp_set.create(
            provider="google",
            name="google",
            client_id="1234567890",
            secret="0987654321",
        )

        self.user = User.objects.create_user(username="admin", password="secret")

    def test_logged_out_user_sees_sign_in_link(self):
        response = self.client.get("/", follow=True)
        self.assertContains(
            response, '<a href="%s">Login</a>' % reverse("account_login"), html=True
        )
        self.assertNotContains(
            response, '<a href="%s">Logout</a>' % reverse("account_logout"), html=True
        )

    def test_normally_logged_in_user_sees_sign_out_link(self):
        self.client.post("/account/login/", {"login": "admin", "password": "secret"})
        response = self.client.get("/")
        self.assertNotContains(
            response, '<a href="%s">Login</a>' % reverse("account_login"), html=True
        )
        self.assertContains(
            response, '<a href="%s">Logout</a>' % reverse("account_logout"), html=True
        )


# TODO: refactor these
class baseLinksTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.current_site = Site.objects.get_current()
        self.SocialApp1 = self.current_site.socialapp_set.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )
        self.SocialApp2 = self.current_site.socialapp_set.create(
            provider="google",
            name="google",
            client_id="1234567890",
            secret="0987654321",
        )

        self.user = User.objects.create_user(username="admin", password="secret")

    def test_logged_out_user_sees_sign_in_link(self):
        response = self.client.get("/", follow=True)
        self.assertContains(
            response, '<a href="%s">Login</a>' % reverse("account_login"), html=True
        )
        self.assertNotContains(
            response, '<a href="%s">Logout</a>' % reverse("account_logout"), html=True
        )

    def test_normally_logged_in_user_sees_sign_out_link(self):
        self.client.post("/account/login/", {"login": "admin", "password": "secret"})
        response = self.client.get("/")
        self.assertNotContains(
            response, '<a href="%s">Login</a>' % reverse("account_login"), html=True
        )
        self.assertContains(
            response, '<a href="%s">Logout</a>' % reverse("account_logout"), html=True
        )


# TODO: these could use some fleshing out
class AllAuthTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.current_site = Site.objects.get_current()
        self.SocialApp1 = self.current_site.socialapp_set.create(
            provider="facebook",
            name="facebook",
            client_id="1234567890",
            secret="0987654321",
        )
        self.SocialApp2 = self.current_site.socialapp_set.create(
            provider="google",
            name="google",
            client_id="1234567890",
            secret="0987654321",
        )

        self.user = User.objects.create_user(username="admin", password="secret")

    # Most of allAuth is tested, only test our integration
    def test_login_page_uses_musr_base(self):
        response = self.client.get("/account/login/")

        self.assertContains(response, "<!-- MUSR base.html -->", status_code=200)
        self.assertTemplateUsed(response, "musr/base.html")

    def test_complain_about_empty_form(self):
        response = self.client.post(
            "/account/login/", {"login": "admin", "password": "wrongsecret"}
        )
        self.assertContains(
            response,
            "The username and/or password you specified are not correct.",
            status_code=200,
        )
        self.assertTemplateUsed(response, "account/login.html")

    def test_complain_about_wrong_password(self):
        response = self.client.post(
            "/account/login/", {"login": "admin", "password": "wrongsecret"}
        )
        self.assertContains(
            response, "The username and/or password you specified are not correct."
        )
        self.assertTemplateUsed(response, "account/login.html")

    def test_complain_about_nonexistent_user(self):
        response = self.client.post(
            "/account/login/", {"login": "fakeuser", "password": "wrongsecret"}
        )
        self.assertContains(
            response, "The username and/or password you specified are not correct."
        )
        self.assertTemplateUsed(response, "account/login.html")

    def test_redirect_to_home_after_logging_in(self):
        response = self.client.post(
            "/account/login/", {"login": "admin", "password": "secret"}
        )
        self.assertRedirects(response, "/")