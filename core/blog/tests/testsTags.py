import random
import json
from faker import Faker
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import create_tag, create_user

fake = Faker()


class TestTagModel(TestCase):

    def setUp(self):
        self.user = create_user()
        self.token = RefreshToken.for_user(self.user)

    def test_list_tags(self):
        count = random.randint(1, 10)
        tags = [create_tag(user=self.user) for _ in range(count)]
        url = reverse("blog:tags.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("tags")), count)

    def test_create_tag(self):
        url = reverse("blog:tags.create")
        response = self.client.post(
            url,
            data={"name": fake.word()},
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
        )
        self.assertEqual(response.status_code, 201)

    def test_tag_detail(self):
        posts_count = random.randint(1, 10)
        tag = create_tag(posts_count=posts_count, user=self.user)
        url = reverse("blog:tags.detail", kwargs={"pk": tag.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("tag").get("name"), tag.name)

    def test_update_tag(self):
        tag = create_tag(user=self.user)
        url = reverse("blog:tags.update", kwargs={"pk": tag.pk})
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

    def test_delete_tag(self):
        tag = create_tag(user=self.user)
        url = reverse("blog:tags.delete", kwargs={"pk": tag.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Tag deleted successfully!")
