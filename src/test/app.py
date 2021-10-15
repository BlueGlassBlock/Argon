import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..")))


from graia.broadcast import Broadcast
from loguru import logger

from graia.argon import ArgonMiraiApplication
from graia.argon.adapter import DebugAdapter
from graia.argon.event.message import FriendMessage
from graia.argon.message.chain import MessageChain
from graia.argon.model import Friend, MiraiSession

if __name__ == "__main__":
    url, account, verify_key = (
        open(os.path.join(__file__, "..", "test.temp"), "r").read().split(" ")
    )

    loop = asyncio.new_event_loop()
    loop.set_debug(True)
    bcc = Broadcast(loop=loop)
    adapter = DebugAdapter(bcc, MiraiSession(url, account, verify_key))
    app = ArgonMiraiApplication(bcc, adapter)

    @bcc.receiver(FriendMessage)
    async def print_msg(
        app: ArgonMiraiApplication, chain: MessageChain, friend: Friend
    ):
        logger.info(f"[{await app.getFriendProfile(friend)}] -> {chain.asDisplay()}")
        await app.sendFriendMessage(friend, MessageChain.create("Hello, World!"))

    async def main():
        await app.launch()
        logger.debug(await app.getVersion())
        logger.debug(await app.getBotProfile())
        group_list = await app.getGroupList()
        logger.debug(group_list)
        friend_list = await app.getFriendList()
        logger.debug(friend_list)
        member_list = await app.getMemberList(group_list[0])
        logger.debug(member_list)
        logger.debug(await app.getFriendProfile(friend_list[0]))
        logger.debug(await app.getMemberProfile(member_list[0], group_list[0]))
        logger.debug(await app.getMemberProfile(member_list[0]))
        logger.debug(
            await app.listFile(group_list[0], size=1024, with_download_info=True)
            # Fetching file info is VERY time consuming
        )
        await app.lifecycle()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(app.stop())
