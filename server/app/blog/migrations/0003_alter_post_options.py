# Generated by Django 4.2.5 on 2023-10-09 07:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_post_cover_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-created_at"],
                "permissions": [("publish_post", "Can publish post")],
                "verbose_name": "文章",
                "verbose_name_plural": "文章",
            },
        ),
    ]