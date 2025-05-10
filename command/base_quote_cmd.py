from ..imports import *
from ..interface.message_handle import (
    pick_received_msg,
)

matcher_listener = on_message(priority=15, block=False, permission=quote_permission)
@matcher_listener.handle()
async def f_listener(event: GroupME, bot: Bot):
    """
    监听群组消息，处理可能的语录收集
    """
    await pick_received_msg(event, bot)