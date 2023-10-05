from django.conf import settings
from django.db import models

from server.utils.django.models import BaseModel

USER_MODEL = settings.AUTH_USER_MODEL


class Post(BaseModel):
    slug = models.SlugField("網址代稱", max_length=255, unique=True)
    author = models.ForeignKey(
        USER_MODEL,
        verbose_name="作者",
        on_delete=models.CASCADE,
    )
    title = models.CharField("標題", max_length=255)
    content = models.TextField("內文")
    published_at = models.DateTimeField("發布時間", null=True, blank=True)
    published = models.BooleanField("是否發布", default=False)
    tags = models.ManyToManyField(
        "Tag",
        verbose_name="標籤",
        blank=True,
        related_name="posts",
    )
    categories = models.ManyToManyField(
        "Category",
        verbose_name="分類",
        blank=True,
        related_name="posts",
    )
    cover_image = models.ImageField(
        "封面圖片",
        upload_to="post/cover_image/%Y%m%d/",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ["-created_at"]


class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        verbose_name="文章",
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="上層留言",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        USER_MODEL,
        verbose_name="作者",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    content = models.TextField("內文")

    def __str__(self) -> str:
        return self.content

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = "留言"
        ordering = ["-created_at"]


class Tag(BaseModel):
    name = models.CharField("標籤名稱", max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "標籤"
        verbose_name_plural = "標籤"
        ordering = ["-created_at"]


class Category(BaseModel):
    slug = models.SlugField("網址代稱", max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        verbose_name="上層分類",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField("分類名稱", max_length=255)

    def __str__(self) -> str:
        if self.parent:
            return f"{self.parent}/{self.name}"
        return self.name

    class Meta:
        verbose_name = "分類"
        verbose_name_plural = "分類"
        ordering = ["-created_at"]
