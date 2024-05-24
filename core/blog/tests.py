import random
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker

from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User

fake = Faker()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = self.create_user()

    def create_user(self):
        return User.objects.create(username=fake.word(), email=fake.email())

    def create_posts(self, user: User, count: int = 1) -> list[Post]:
        category = self.create_category()
        return [
            Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                user=user,
                category=category,
            )
            for _ in range(count)
        ]

    def create_category(self):
        return Category.objects.create(name=fake.word())

    def create_tag(self, count: int = 1):
        return [Tag.objects.create(name=fake.word()) for _ in range(count)]

    def test_login(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_list_of_posts(self):
        count = random.randint(1, 10)
        posts = self.create_posts(self.user, count)
        refresh = RefreshToken.for_user(self.user)
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("posts")), count)

    def test_post_detail(self):
        post = self.create_posts(self.user)[0]
        refresh = RefreshToken.for_user(self.user)
        url = reverse("blog:posts.detail", kwargs={"pk": post.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), post.title)

    def test_post_create(self):
        refresh = RefreshToken.for_user(self.user)
        url = reverse("blog:posts.create")
        category = self.create_category()
        tags = self.create_tag(random.randint(1, 5))
        data = {
            "title": fake.sentence(),
            "content": fake.text(),
            "category_id": category.id,
            "tags": [tag.id for tag in tags],
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), data.get("title"))
