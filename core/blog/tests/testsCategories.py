import random
import json
from faker import Faker
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import create_category, create_user

fake = Faker()


class TestCategoryModel(TestCase):

    def setUp(self):
        self.user = create_user()
        self.token = RefreshToken.for_user(self.user)

    def test_list_categories(self):
        count = random.randint(1, 10)
        categories = [create_category() for _ in range(count)]
        url = reverse("blog:categories.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("categories")), count)

    def test_create_category(self):
        url = reverse("blog:categories.create")
        response = self.client.post(
            url,
            data={"name": fake.word()},
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_category_detail(self):
        category = create_category()
        url = reverse("blog:categories.detail", kwargs={"pk": category.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("category").get("name"), category.name)

    def test_update_category(self):
        category = create_category()
        url = reverse("blog:categories.update", kwargs={"pk": category.pk})
        data = {
            "name": fake.word(),
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_category(self):
        category = create_category()
        url = reverse("blog:categories.delete", kwargs={"pk": category.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Category deleted successfully!")

    def test_category_posts(self):
        post_count = random.randint(1, 10)
        category = create_category(posts_count=post_count, user=self.user)
        url = reverse("blog:categories.posts", kwargs={"pk": category.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("posts")), post_count)
