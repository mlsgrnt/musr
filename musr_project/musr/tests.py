from django.test import TestCase, Client
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Create your tests here.
class TravisTesterTestCase(TestCase):
    def test_unit_tests_are_understood_and_can_pass(self):
        """Unit tests run and are able to pass"""
        test_value = 5
        self.assertEqual(test_value, 5)


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
