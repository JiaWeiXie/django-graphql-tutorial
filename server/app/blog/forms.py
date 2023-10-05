from django import forms
from django.contrib.auth import get_user_model

from server.app.blog import models as blog_models

USER_MODEL = get_user_model()


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=blog_models.Tag.objects.all(),
        to_field_name="name",
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=blog_models.Category.objects.all(),
        to_field_name="slug",
    )
    author = forms.ModelChoiceField(
        queryset=USER_MODEL.objects.all(),
        to_field_name="username",
    )

    class Meta:
        model = blog_models.Post
        fields = (
            "title",
            "content",
            "published",
            "published_at",
            "slug",
        )
