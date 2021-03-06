# Argon
[![Licence](https://img.shields.io/github/license/BlueGlassBlock/Argon)](https://github.com/BlueGlassBlock/Argon/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?labelColor=ef8336)](https://pycqa.github.io/isort/)

______________________

一个基于 [`graia-broadcast`](https://github.com/GraiaProject/BroadcastControl) 和
[`mirai-api-http v2`](https://github.com/project-mirai/mirai-api-http) 的 Python SDK。

**本项目适用于 mirai-api-http 2.0 以上版本**。

目前仍处于开发阶段，内部接口可能会有较大的变化。

## The Stasis / 停滞

**为维持 `GraiaProject` 统一性，本项目正式由 `Argon` 更名为 [`Ariadne`](https://github.com/GraiaProject/Ariadne)**

**本项目已Archive.**

**[Ariadne repo link](https://github.com/GraiaProject/Ariadne)**

## 安装
已移除 PyPI 包

## 鸣谢&相关项目
> 这些项目也很棒, 去他们的项目页看看, 点个 `Star` 以鼓励他们的开发工作, 毕竟没有他们也没有 `Argon`.

特别感谢 [`mamoe`](https://github.com/mamoe) 给我们带来这些精彩的项目:
 - [`mirai`](https://github.com/mamoe/mirai): 一个高性能, 高可扩展性的 QQ 协议库
 - [`mirai-console`](https://github.com/mamoe/mirai-console): 一个基于 `mirai` 开发的插件式可扩展开发平台
 - [`mirai-api-http`](https://github.com/project-mirai/mirai-api-http): 为本项目提供与 `mirai` 交互方式的 `mirai-console` 插件

[`GraiaProject`](https://github.com/GraiaProject) 的其他项目:
 - [`Broadcast Control`](https://github.com/GraiaProject/BroadcastControl): 扩展性强大, 模块间低耦合, 高灵活性的事件系统支持，是 `Argon` 的底层。**兼容**
 - [`Components`](https://github.com/GraiaProject/Components): 简单的消息链元素选择器 **不兼容，将提供移植**
 - [`Template`](https://github.com/GraiaProject/Template): 消息模板 **不兼容，将提供移植**
 - [`Saya`](https://github.com/GraiaProject/Saya) 间接但简洁的模块管理系统. **兼容**
 - [`Scheduler`](https://github.com/GraiaProject/Scheduler): 简洁的基于 `asyncio` 的定时任务实现. **兼容**
 - [`Application`](https://github.com/GraiaProject/Application/) (a.k.a v4): 本项目的结构基础，支持 `mirai-api-http v1.x` 版本 。**不完全兼容，建议参照项目内实现名称进行移植工作**
 - [`Avilla`](https://github.com/GraiaProject/Avilla/) (a.k.a v5): 
 下一代即时通讯框架。`The Future`。**不兼容**

`Argon` 在开发中还参考了如下项目：
 - [`YiriMirai`](https://github.com/YiriMiraiProject/YiriMirai/): 本项目的 [`adapter`](./src/graia/argon/adapter.py) 及 [`MessageChain`](./src/graia/argon/message/chain.py) 实现参考。

### 许可证

[`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 是本项目的开源许可证.