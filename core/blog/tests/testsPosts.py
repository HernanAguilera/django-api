import random
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from faker import Faker

from .utils import (
    create_user,
    create_posts,
    create_category,
    create_tag,
    create_comment,
)

fake = Faker()


class PostModelTest(TestCase):

    def setUp(self):
        self.user = create_user()
        self.token = RefreshToken.for_user(self.user)

    def test_login(self):
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_list_of_posts(self):
        count = random.randint(1, 10)
        posts = create_posts(self.user, count)
        url = reverse("blog:posts.index")
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("posts")), count)

    def test_post_detail(self):
        post = create_posts(self.user)[0]
        url = reverse("blog:posts.detail", kwargs={"pk": post.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("post").get("title"), post.title)

    def test_post_create(self):
        url = reverse("blog:posts.create")
        category = create_category()
        tags = create_tag(random.randint(1, 5))
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

    def test_post_update_by_owner(self):
        post = create_posts(self.user)[0]
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

    def test_post_update_by_not_owner(self):
        post = create_posts(self.user)[0]
        user = create_user()
        token = RefreshToken.for_user(user)
        url = reverse("blog:posts.update", kwargs={"pk": post.pk})
        data = {"title": fake.sentence(), "content": fake.text()}
        response = self.client.put(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data.get("message"), "You are not the owner of this post!"
        )

    def test_post_delete_by_owner(self):
        post = create_posts(self.user)[0]
        url = reverse("blog:posts.delete", kwargs={"pk": post.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Post deleted successfully!")

    def test_post_delete_by_not_owner(self):
        post = create_posts(self.user)[0]
        user = create_user()
        token = RefreshToken.for_user(user)
        url = reverse("blog:posts.delete", kwargs={"pk": post.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data.get("message"), "You are not the owner of this post!"
        )

    def test_comments_of_post(self):
        post = create_posts(self.user)[0]
        comments_count = random.randint(1, 10)
        create_comment(post, self.user, comments_count)
        url = reverse("blog:comments", kwargs={"pk": post.pk})
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get("comments")), post.comments.count())

    def test_add_comment_to_post(self):
        post = create_posts(self.user)[0]
        url = reverse("blog:comments.create", kwargs={"pk": post.pk})
        data = {"body": fake.text()}
        response = self.client.post(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("comment").get("body"), data.get("body"))

    def test_update_comment_by_owner(self):
        post = create_posts(self.user)[0]
        comment = create_comment(post, self.user)[0]
        url = reverse("blog:comments.update", kwargs={"pk": comment.pk})
        data = {"body": fake.text()}
        response = self.client.put(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("comment").get("body"), data.get("body"))

    def test_update_comment_by_not_owner(self):
        post = create_posts(self.user)[0]
        comment = create_comment(post, self.user)[0]
        user = create_user()
        token = RefreshToken.for_user(user)
        url = reverse("blog:comments.update", kwargs={"pk": comment.pk})
        data = {"body": fake.text()}
        response = self.client.put(
            url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=f"Bearer {token.access_token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data.get("message"), "You are not the owner of this comment!"
        )

    def test_delete_comment_by_owner(self):
        post = create_posts(self.user)[0]
        comment = create_comment(post, self.user)[0]
        url = reverse("blog:comments.delete", kwargs={"pk": comment.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Comment deleted successfully!")

    def test_delete_comment_by_not_owner(self):
        post = create_posts(self.user)[0]
        comment = create_comment(post, self.user)[0]
        user = create_user()
        token = RefreshToken.for_user(user)
        url = reverse("blog:comments.delete", kwargs={"pk": comment.pk})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Bearer {token.access_token}"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data.get("message"), "You are not the owner of this comment!"
        )
