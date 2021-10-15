import typing

from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.entities.event import Dispatchable
from graia.broadcast.interfaces.dispatcher import DispatcherInterface

if typing.TYPE_CHECKING:
    from graia.argon import ArgonMiraiApplication


class ApplicationLaunched(Dispatchable):
    app: "ArgonMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface[ApplicationLaunched]"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app


class ApplicationShutdowned(Dispatchable):
    app: "ArgonMiraiApplication"

    def __init__(self, app) -> None:
        self.app = app

    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface: "DispatcherInterface[ApplicationShutdowned]"):
            from .. import GraiaMiraiApplication

            if interface.annotation is GraiaMiraiApplication:
                return interface.event.app
