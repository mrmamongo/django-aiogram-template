"""
ASGI config for template project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django_asgi_lifespan.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'template.settings')

django_application = get_asgi_application()
async def application(scope, receive, send):
    if scope["type"] in {"http", "lifespan"}:
        await django_application(scope, receive, send)
    else:
        raise NotImplementedError(
            f"Unknown scope type {scope['type']}"
        )