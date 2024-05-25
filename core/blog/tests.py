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

    def setUp(self):
        self.user = self.create_user()
        self.token = RefreshToken.for_user(self.user)

    def test_login(self):
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_list_of_posts(self):
        count = random.randint(1, 10)
        posts = self.create_posts(self.user, count)
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("posts")), count)

    def test_post_detail(self):
        post = self.create_posts(self.user)[0]
        url = reverse("blog:posts.detail", kwargs={"pk": post.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), post.title)

    def test_post_create(self):
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
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), data.get("title"))

    def test_post_update(self):
        post = self.create_posts(self.user)[0]
        url = reverse("blog:posts.update", kwargs={"pk": post.pk})
        data = {"title": fake.sentence(), "content": fake.text()}
        response = self.client.put(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), data.get("title"))

    def test_post_delete(self):
        post = self.create_posts(self.user)[0]
        url = reverse("blog:posts.delete", kwargs={"pk": post.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Post deleted successfully!")
