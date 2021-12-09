from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Snack
from django.urls import reverse

class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="trad", email="trad@gmail.com", password="pass"
        )

        self.snack = Snack.objects.create(
            title="shawarma", description="wow", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "shawarma")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "shawarma")
        self.assertEqual(f"{self.snack.purchaser}", "trad")
        self.assertEqual(self.snack.description, "wow")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shawarma")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        # no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "trad")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Mansaf",
                "description": "mmm",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Mansaf")

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Batata","description":"delecious","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)
