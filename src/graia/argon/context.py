from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

from graia.argon.model import UploadMethod

if TYPE_CHECKING:
    from asyncio.events import AbstractEventLoop

    from graia.broadcast import Broadcast

    from graia.argon import ArgonMiraiApplication
    from graia.argon.adapter import Adapter
    from graia.argon.event import MiraiEvent


application_ctx: ContextVar["ArgonMiraiApplication"] = ContextVar("application")
adapter_ctx: ContextVar["Adapter"] = ContextVar("adapter")
event_ctx: ContextVar["MiraiEvent"] = ContextVar("event")
event_loop_ctx: ContextVar["AbstractEventLoop"] = ContextVar("event_loop")
broadcast_ctx: ContextVar["Broadcast"] = ContextVar("broadcast")
upload_method_ctx: ContextVar["UploadMethod"] = ContextVar("upload_method")


@contextmanager
def enter_message_send_context(method: UploadMethod):
    t = upload_method_ctx.set(method)
    yield
    upload_method_ctx.reset(t)


@contextmanager
def enter_context(app=None, event=None):
    token_app = None
    token_event = None
    token_loop = None
    token_bcc = None
    token_adapter = None

    if app:
        token_app = application_ctx.set(app)
        token_loop = event_loop_ctx.set(app.broadcast.loop)
        token_bcc = broadcast_ctx.set(app.broadcast)
        token_adapter = adapter_ctx.set(app.adapter)
    if event:
        token_event = event_ctx.set(event)

    yield

    try:
        if token_app:
            application_ctx.reset(token_app)
        if token_adapter:
            adapter_ctx.reset(token_adapter)
        if all([token_event, token_loop, token_bcc]):
            event_ctx.reset(token_event)
            event_loop_ctx.reset(token_loop)
            broadcast_ctx.reset(token_bcc)
    except ValueError:
        pass
