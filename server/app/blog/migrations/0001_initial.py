# Generated by Django 4.2.5 on 2023-09-28 17:29

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                (
                    "motified_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改時間"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="網址代稱"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="分類名稱")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="blog.category",
                        verbose_name="上層分類",
                    ),
                ),
            ],
            options={
                "verbose_name": "分類",
                "verbose_name_plural": "分類",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                (
                    "motified_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改時間"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="標籤名稱"),
                ),
            ],
            options={
                "verbose_name": "標籤",
                "verbose_name_plural": "標籤",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                (
                    "motified_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改時間"),
                ),
                (
                    "slug",
                    models.SlugField(max_length=255, unique=True, verbose_name="網址代稱"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="標題")),
                ("content", models.TextField(verbose_name="內文")),
                (
                    "published_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="發布時間"),
                ),
                ("published", models.BooleanField(default=False, verbose_name="是否發布")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="作者",
                    ),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="posts",
                        to="blog.category",
                        verbose_name="分類",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="posts",
                        to="blog.tag",
                        verbose_name="標籤",
                    ),
                ),
            ],
            options={
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                (
                    "motified_at",
                    models.DateTimeField(auto_now=True, verbose_name="修改時間"),
                ),
                ("content", models.TextField(verbose_name="內文")),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="作者",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.comment",
                        verbose_name="上層留言",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.post",
                        verbose_name="文章",
                    ),
                ),
            ],
            options={
                "verbose_name": "留言",
                "verbose_name_plural": "留言",
                "ordering": ["-created_at"],
            },
        ),
    ]