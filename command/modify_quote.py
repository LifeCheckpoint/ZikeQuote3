from ..imports import *
from ..interface.quote_handle import add_quote, remove_quote, QuoteInfoV2
from ..interface.message_handle import get_group_member_cardname, get_mapping

add_quote_alias = {"add_quote", "quote_add", "添加语录", "新增语录", "语录添加"}
matcher_add_quote = on_command("加语录", aliases=add_quote_alias, priority=10, block=True, permission=quote_permission)
@matcher_add_quote.handle()
async def f_add_quote(event: GroupME, bot: Bot):
    """
    添加语录

    语录添加方式有两种，通过是否有 reply 进行判断：
    1. `(reply) /加语录`
    2. `/加语录 @某人 语录内容`
    """
    # 判断 reply
    reply = event.reply

    if reply != None:
        reply_msg = reply.message.extract_plain_text().strip()
        if reply_msg == "":
            await mfinish(matcher_add_quote, msg_add_quote_reply_args_missing)
        
        try:
            add_quote(event.group_id, QuoteInfoV2(
                quote_id = reply.message_id,
                author_id = reply.sender.user_id or -1,
                author_name = reply.sender.nickname or "",
                author_card = await get_group_member_cardname(event.group_id, reply.sender.user_id or -1, bot) or "",
                time_stamp = event.time,
                quote = reply_msg,
                reason = "手动添加",
                show_time = 0,
                recommend = False,
                ext_data = None
            ))
        except Exception as e:
            await mfinish(matcher_add_quote, msg_add_quote_failed, error=str(e))

        await mfinish(matcher_add_quote, msg_add_quote_success, author=reply.sender.nickname)

    else:
        # 检查 At 消息段
        # TODO
        pass

remove_quote_alias = {"remove_quote", "quote_remove", "删除语录", "语录删除"}
matcher_remove_quote = on_command("删语录", aliases=remove_quote_alias, priority=10, block=True, permission=quote_permission)
@matcher_remove_quote.handle()
async def f_remove_quote(event: GroupME, bot: Bot):
    """
    删除语录

    语录删除方式：
    `(reply) /删语录`
    """
    # 判断权限
    if event.sender not in cfg.quote_managers:
        await mfinish(matcher_remove_quote, msg_no_permission, event="删语录")
    
    # 判断 reply
    reply = event.reply
    if reply == None:
        await mfinish(matcher_remove_quote, msg_remove_quote_reply_args_missing)
        return

    # 获取语录 ID
    quote_id = get_mapping(event.group_id, reply.message_id)
    if quote_id == None:
        await mfinish(matcher_remove_quote, msg_remove_quote_not_found)
        return
    
    # 删除语录
    result = remove_quote(event.group_id, quote_id)
    if result:
        await mfinish(matcher_remove_quote, msg_remove_quote_success, author=get_group_member_cardname(event.group_id, event.sender.user_id or -1, bot))
    else:
        await mfinish(matcher_remove_quote, msg_remove_quote_failed)