from faker import Faker
from django.contrib.auth.models import User
from ..models import Post, Category, Tag, Comment

fake = Faker()


def create_user():
    return User.objects.create(username=fake.word(), email=fake.email())


def create_posts(user: User, count: int = 1) -> list[Post]:
    category = create_category()
    return [
        Post.objects.create(
            title=fake.sentence(),
            content=fake.text(),
            user=user,
            category=category,
        )
        for _ in range(count)
    ]


def create_category():
    return Category.objects.create(name=fake.word())


def create_tag(count: int = 1):
    return [Tag.objects.create(name=fake.word()) for _ in range(count)]


def create_comment(post: Post, user: User, count: int = 1) -> list[Comment]:
    return [
        Comment.objects.create(
            body=fake.text(),
            post=post,
            user=user,
        )
        for _ in range(count)
    ]
