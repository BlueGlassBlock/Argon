from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union
from loguru import logger
from pydantic import BaseModel, Field, validator
from pydantic.main import BaseConfig, Extra
from pydantic.networks import AnyHttpUrl
from typing_extensions import Literal
from yarl import URL

if TYPE_CHECKING:
    from graia.argon import ArgonMiraiApplication


class ArgonBaseModel(BaseModel):
    class Config(BaseConfig):
        extra = Extra.allow


class ChatLogConfig(BaseModel):
    enabled: bool = True
    log_level: str = "INFO"
    group_message_log_format: str = "{bot_id}: [{group_name}({group_id})] {member_name}({member_id}) -> {message_string}"
    friend_message_log_format: str = (
        "{bot_id}: [{friend_name}({friend_id})] -> {message_string}"
    )
    temp_message_log_format: str = "{bot_id}: [{group_name}({group_id}.{member_name}({member_id})] -> {message_string}"
    other_client_message_log_format: str = (
        "{bot_id}: [{platform_name}({platform_id})] -> {message_string}"
    )
    stranger_message_log_format: str = (
        "{bot_id}: [{stranger_name}({stranger_id})] -> {message_string}"
    )

    def initialize(self, app: "ArgonMiraiApplication"):
        from graia.argon.event.message import (
            GroupMessage,
            FriendMessage,
            TempMessage,
            OtherClientMessage,
            StrangerMessage,
        )

        @app.broadcast.receiver(GroupMessage)
        def log_group_message(event: GroupMessage):
            logger.log(
                self.log_level,
                self.group_message_log_format.format_map(
                    dict(
                        group_id=event.sender.group.id,
                        group_name=event.sender.group.name,
                        member_id=event.sender.id,
                        member_name=event.sender.name,
                        member_permission=event.sender.permission.name,
                        bot_id=app.mirai_session.account,
                        bot_permission=event.sender.group.accountPerm.name,
                        message_string=event.messageChain.asDisplay().__repr__(),
                    )
                ),
            )

        @app.broadcast.receiver(FriendMessage)
        def log_friend_message(event: FriendMessage):
            logger.log(
                self.log_level,
                self.friend_message_log_format.format_map(
                    dict(
                        bot_id=app.mirai_session.account,
                        friend_name=event.sender.nickname,
                        friend_id=event.sender.id,
                        message_string=event.messageChain.asDisplay().__repr__(),
                    )
                ),
            )

        @app.broadcast.receiver(TempMessage)
        def log_temp_message(event: TempMessage):
            logger.log(
                self.log_level,
                self.temp_message_log_format.format_map(
                    dict(
                        group_id=event.sender.group.id,
                        group_name=event.sender.group.name,
                        member_id=event.sender.id,
                        member_name=event.sender.name,
                        member_permission=event.sender.permission.name,
                        bot_id=app.mirai_session.account,
                        bot_permission=event.sender.group.accountPerm.name,
                        message_string=event.messageChain.asDisplay().__repr__(),
                    )
                ),
            )

        @app.broadcast.receiver(StrangerMessage)
        def log_stranger_message(event: StrangerMessage):
            logger.log(
                self.log_level,
                self.stranger_message_log_format.format_map(
                    bot_id=app.mirai_session.account,
                    stranger_name=event.sender.nickname,
                    stranger_id=event.sender.id,
                    message_string=event.messageChain.asDisplay().__repr__(),
                ),
            )

        @app.broadcast.receiver(OtherClientMessage)
        def log_other_client_message(event: OtherClientMessage):
            logger.log(
                self.log_level,
                self.other_client_message_log_format.format_map(
                    bot_id=app.mirai_session.account,
                    platform_name=event.sender.platform,
                    platform_id=event.sender.id,
                    message_string=event.messageChain.asDisplay().__repr__(),
                ),
            )


class MiraiSession(ArgonBaseModel):
    """
    ?????????????????????????????????, ?????????????????????????????????.

    Attributes:
        host (AnyHttpUrl): `mirai-api-http` ??????????????????????????????
        account (int): ?????????????????????????????? ID, ???????????? `singleMode` ????????????, ?????????????????????.
        verify_key (str): ??? `mirai-api-http` ?????????????????????, ???????????????????????????????????????, ?????? mirai-api-http ??????????????? `enableVerify`.
        session_key (str, optional): ????????????, ???????????????????????????????????????????????????.
    """

    host: AnyHttpUrl
    single_mode: bool = False
    account: Optional[int] = None
    verify_key: Optional[str] = None
    session_key: Optional[str] = None
    version: Optional[str] = None

    def __init__(
        self,
        host: AnyHttpUrl,
        account: Optional[int] = None,
        verify_key: Optional[str] = None,
        *,
        single_mode: bool = False,
    ) -> None:
        super().__init__(
            host=host, account=account, verify_key=verify_key, single_mode=single_mode
        )

    def url_gen(self, route: str) -> str:
        return str(URL(self.host) / route)


class Friend(ArgonBaseModel):
    "?????? Tencent QQ ????????????."

    id: int
    nickname: str
    remark: str


class MemberPerm(Enum):
    "?????????????????????????????????????????????"

    Member = "MEMBER"  # ????????????
    Administrator = "ADMINISTRATOR"  # ?????????
    Owner = "OWNER"  # ??????


class Group(ArgonBaseModel):
    "?????? Tencent QQ ????????????."

    id: int
    name: str
    accountPerm: MemberPerm = Field(..., alias="permission")


class Member(ArgonBaseModel):
    "????????????????????????????????????????????????, ??????????????????, ????????????, ??????????????????, ??????ID."

    id: int
    name: str = Field(..., alias="memberName")
    permission: MemberPerm
    specialTitle: Optional[str] = None
    joinTimestamp: Optional[int] = None
    lastSpeakTimestamp: Optional[int] = None
    mutetimeRemaining: Optional[int] = None
    group: Group


class GroupConfig(ArgonBaseModel):
    "?????????????????????????????????."

    name: str = ""
    announcement: str = ""
    confessTalk: bool = False
    allowMemberInvite: bool = False
    autoApprove: bool = False
    anonymousChat: bool = False

    # ?????? json ?????????????????? exclude_none=True.

    class Config:
        allow_mutation = True


class MemberInfo(ArgonBaseModel):
    "????????????????????????????????????, ?????????????????????/????????????."

    name: str = ""
    specialTitle: str = ""

    # ?????? json ?????????????????? exclude_none=True.

    class Config:
        allow_mutation = True


class DownloadInfo(ArgonBaseModel):
    sha: str = ""
    md5: str = ""
    download_times: int = Field(..., alias="downloadTimes")
    uploader_id: int = Field(..., alias="uploaderId")
    upload_time: datetime = Field(..., alias="uploadTime")
    last_modify_time: datetime = Field(..., alias="lastModifyTime")
    url: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }


class FileInfo(ArgonBaseModel):
    "????????????????????????"

    name: str = ""
    path: str = ""
    id: Optional[str] = ""
    parent: Optional["FileInfo"] = None
    contact: Optional[Union[Group, Friend]] = None
    is_file: bool = Field(..., alias="isFile")
    is_directory: bool = Field(..., alias="isDirectory")
    download_info: Optional[DownloadInfo] = Field(None, alias="downloadInfo")

    @validator("contact", pre=True, allow_reuse=True)
    def _(cls, val: Optional[dict]):
        if not val:
            return None
        else:
            if "remark" in val:  # Friend
                return Friend.parse_obj(val)
            else:  # Group
                return Group.parse_obj(val)


FileInfo.update_forward_refs(FileInfo=FileInfo)


class UploadMethod(Enum):
    """????????? `uploadImage` ??? `uploadVoice` ?????????????????????????????????"""

    Friend = "friend"
    Group = "group"
    Temp = "temp"


class CallMethod(Enum):
    GET = "GET"
    POST = "POST"
    RESTGET = "get"
    RESTPOST = "update"
    MULTIPART = "multipart"


class Client(ArgonBaseModel):
    """
    ?????????????????????
    """

    id: int
    platform: str


class Profile(ArgonBaseModel):
    """
    ?????????????????????????????????
    """

    nickname: str
    email: Optional[str]
    age: Optional[int]
    level: int
    sign: str
    sex: Literal["UNKNOWN", "MALE", "FEMALE"]


class BotMessage(ArgonBaseModel):
    messageId: int
