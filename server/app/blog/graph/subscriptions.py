import typing

import strawberry
from channels.db import database_sync_to_async
from django.conf import settings
from strawberry.types import Info

from server.app.blog import models as blog_models
from server.app.blog.graph import types as blog_types


@database_sync_to_async
def _get_post(id: str) -> blog_models.Post | None:  # noqa: A002
    try:
        return blog_models.Post.objects.get(id=id)
    except blog_models.Post.DoesNotExist:
        return None


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_notify(
        self,
        info: Info,
    ) -> typing.AsyncGenerator[blog_types.PostNotification, None]:
        ws = info.context["ws"]
        channel_layer = ws.channel_layer
        await channel_layer.group_add(settings.POSTS_CHANNEL, ws.channel_name)

        async with ws.listen_to_channel(
            "chat.message",
            groups=[settings.POSTS_CHANNEL],
        ) as cm:
            async for message in cm:
                post = await _get_post(message["post_id"])
                if post:
                    yield blog_types.PostNotification(
                        id=post.pk,
                        title=post.title,
                        publish_at=post.published_at,
                    )
