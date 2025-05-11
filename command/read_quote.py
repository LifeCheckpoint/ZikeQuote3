from ..imports import *
from ..interface.message_handle import (
    pick_received_msg,
    read_msg_and_pickup,
    add_mapping,
    get_mapping,
)
from ..interface.quote_handle import (
    QuoteInfoV2,
    get_random_quote,
)

matcher_listener = on_message(priority=15, block=False, permission=quote_permission)
@matcher_listener.handle()
async def f_listener(event: GroupME, bot: Bot):
    """
    监听群组消息，处理可能的语录收集
    """
    _ = await pick_received_msg(event, bot)


random_quote_alias = {"quote", "随机语录"}
matcher_random_quote = on_command("语录", aliases=random_quote_alias, priority=10, block=True, permission=quote_permission)
@matcher_random_quote.handle()
async def f_random_quote(event: GroupME, bot: Bot):
    """
    随机语录
    """
    key = event.get_plaintext().strip() # 默认为搜索名字+内容
    if key == "":
        result: QuoteInfoV2 = get_random_quote(event.group_id) # type: ignore
    else:
        filt: Callable[[QuoteInfoV2], bool] = lambda quote: key in quote.quote or key in quote.author_name or key in quote.author_card
        result: QuoteInfoV2 = get_random_quote(event.group_id, filt) # type: ignore

    if not result:
        await mfinish(matcher_random_quote, msg_quote_not_found, key=key)
    else:
        send_msg = await msend(matcher_random_quote, msg_send_quote, author=result.author_name, quote=result.quote)
        add_mapping(event.group_id, send_msg.message_id, result.quote_id)


update_quote_alias = {"更新语录", "语录更新", "强制更新语录", "强制语录更新"}
matcher_update_quote = on_command("语录强制更新", aliases=update_quote_alias, priority=10, block=True, permission=quote_permission)
@matcher_update_quote.handle()
async def f_update_quote(event: GroupME):
    """
    强制更新语录
    """
    await msend(matcher_update_quote, msg_quote_on_update)
    result = await read_msg_and_pickup(event.group_id)
    if result:
        await mfinish(matcher_update_quote, msg_quote_update_success)
    else:
        await mfinish(matcher_update_quote, msg_quote_update_failed)
