import sys
from typing import Any

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import AnyUrl

from app.api.routes.webhook import webhook_router
from app.api.stubs import BotStub, DispatcherStub, SecretStub
from app.settings import settings


def create_app(bot: Bot, dispatcher: Dispatcher, webhook_secret: str) -> FastAPI:
    app = FastAPI()

    app.dependency_overrides.update(
        {
            BotStub: lambda: bot,
            DispatcherStub: lambda: dispatcher,
            SecretStub: lambda: webhook_secret,
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(webhook_router)

    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        "bot": bot,
        **dispatcher.workflow_data,
    }

    async def on_startup(*a: Any, **kw: Any) -> None:  # pragma: no cover
        if settings.DEVELOPMENT:
            from ngrok import ngrok
            port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
            tunnel = await ngrok.connect(port)  # type: ignore[misc]
            public_url = tunnel.url()
            settings.BASE_URL = AnyUrl(public_url)
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*a: Any, **kw: Any) -> None:  # pragma: no cover
        if settings.DEVELOPMENT:
            from ngrok import ngrok
            ngrok.disconnect()
        await dispatcher.emit_shutdown(**workflow_data)

    app.add_event_handler('startup', on_startup)
    app.add_event_handler('shutdown', on_shutdown)


    return app
