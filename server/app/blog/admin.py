from django.contrib import admin

from server.app.blog.models import Category, Comment, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_at", "published"]
    list_filter = ["published_at", "published"]
    search_fields = ["title"]
    autocomplete_fields = ["author", "tags", "categories"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "parent", "content"]
    list_filter = ["post"]
    autocomplete_fields = ["post", "author"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
