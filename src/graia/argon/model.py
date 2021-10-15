from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic.main import BaseConfig, Extra
from pydantic.networks import AnyHttpUrl
from yarl import URL


class ArgonBaseModel(BaseModel):
    class Config(BaseConfig):
        extra = Extra.allow


class MiraiSession(ArgonBaseModel):
    """
    用于描述与上游接口会话, 并存储会话状态的实体类.

    Attributes:
        host (AnyHttpUrl): `mirai-api-http` 服务所在的根接口地址
        account (int): 应用所使用账号的整数 ID, 虽然启用 `singleMode` 时不需要, 但仍然建议填写.
        verify_key (str): 在 `mirai-api-http` 配置流程中定义, 需为相同的值以通过安全验证, 需在 mirai-api-http 配置里启用 `enableVerify`.
        session_key (str, optional): 会话标识, 即会话中用于进行操作的唯一认证凭证.
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
    "描述 Tencent QQ 中的好友."

    id: int
    nickname: str
    remark: str


class MemberPerm(Enum):
    "描述群成员在群组中所具备的权限"

    Member = "MEMBER"  # 普通成员
    Administrator = "ADMINISTRATOR"  # 管理员
    Owner = "OWNER"  # 群主


class Group(ArgonBaseModel):
    "描述 Tencent QQ 中的群组."

    id: int
    name: str
    accountPerm: MemberPerm = Field(..., alias="permission")


class Member(ArgonBaseModel):
    "描述用户在群组中所具备的有关状态, 包括所在群组, 群中昵称, 所具备的权限, 唯一ID."

    id: int
    name: str = Field(..., alias="memberName")
    permission: MemberPerm
    specialTitle: Optional[str] = None
    joinTimestamp: Optional[int] = None
    lastSpeakTimestamp: Optional[int] = None
    mutetimeRemaining: Optional[int] = None
    group: Group


class GroupConfig(ArgonBaseModel):
    "描述群组各项功能的设置."

    name: str = ""
    announcement: str = ""
    confessTalk: bool = False
    allowMemberInvite: bool = False
    autoApprove: bool = False
    anonymousChat: bool = False

    # 调用 json 方法时记得加 exclude_none=True.

    class Config:
        allow_mutation = True


class MemberInfo(ArgonBaseModel):
    "描述群组成员的可修改状态, 修改需要管理员/群主权限."

    name: str = ""
    specialTitle: str = ""

    # 调用 json 方法时记得加 exclude_none=True.

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
    "群组文件详细信息"

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
    """用于向 `uploadImage` 或 `uploadVoice` 方法描述图片的上传类型"""

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
    指示其他客户端
    """

    id: int
    platform: str


class Profile(ArgonBaseModel):
    """
    指示某个用户的个人资料
    """

    nickname: str
    email: Optional[str]
    age: Optional[int]
    level: int
    sign: str
    sex: Literal["UNKNOWN", "MALE", "FEMALE"]


class BotMessage(ArgonBaseModel):
    messageId: int
