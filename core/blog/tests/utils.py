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


def create_category(posts_count: int = 0, user: User = None):
    category = Category.objects.create(name=fake.word())
    if posts_count:
        [
            Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                user=user,
                category=category,
            )
            for _ in range(posts_count)
        ]
    return category


def create_tag(posts_count: int = 0, user: User = None):
    tag = Tag.objects.create(name=fake.word())
    category = Category.objects.create(name=fake.word())
    if posts_count:
        for _ in range(posts_count):
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.text(),
                user=user,
                category=category,
            )
            post.tags.add(tag)
    return tag


def create_comment(post: Post, user: User, count: int = 1) -> list[Comment]:
    return [
        Comment.objects.create(
            body=fake.text(),
            post=post,
            user=user,
        )
        for _ in range(count)
    ]
