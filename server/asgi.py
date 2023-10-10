"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from strawberry.channels import GraphQLProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

django_asgi_app = get_asgi_application()

from server.schema import ws_schema  # noqa: E402

application = GraphQLProtocolTypeRouter(
    ws_schema,
    django_application=django_asgi_app,  # type: ignore
    url_pattern="^wsgraphql",
)
