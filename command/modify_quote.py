"""
语录变更相关命令
"""

from ..imports import *
from ..interface.quote_handle import (
    QuoteInfoV2,
    QuoteV2Comment,
    add_quote,
    add_comment,
    remove_quote,
)
from ..interface.message_handle import (
    read_msg_and_pickup,
    get_group_member_cardname,
    get_mapping
)

update_quote_alias = {"更新语录", "语录更新", "强制更新语录", "强制语录更新"}
matcher_update_quote = on_command("语录强制更新", aliases=update_quote_alias, priority=10, block=True, permission=quote_permission) # type: ignore
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


add_quote_alias = {"add_quote", "quote_add", "添加语录", "新增语录", "语录添加"}
matcher_add_quote = on_command("加语录", aliases=add_quote_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_add_quote.handle()
@serial_execution
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
            ))
        except Exception as e:
            await mfinish(matcher_add_quote, msg_add_quote_failed, error=str(e))

        await mfinish(matcher_add_quote, msg_add_quote_success, author=reply.sender.nickname)

    else:
        # 检查 At 消息段
        # TODO
        pass


remove_quote_alias = {"remove_quote", "quote_remove", "删除语录", "语录删除"}
matcher_remove_quote = on_command("删语录", aliases=remove_quote_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_remove_quote.handle()
@serial_execution
async def f_remove_quote(event: GroupME, bot: Bot, arg: Message = CommandArg()):
    """
    删除语录

    语录删除方式：
    1. `(reply) /删语录`
    2. `/删语录 语录ID`
    """
    # 判断权限
    if event.sender not in cfg.quote_managers:
        await mfinish(matcher_remove_quote, msg_no_permission, event="删语录")
    
    # 判断 reply
    reply = event.reply
    key = arg.extract_plain_text().strip()
    if reply == None and key == "":
        await mfinish(matcher_remove_quote, msg_remove_quote_reply_args_missing)
        return
    
    # 获取语录 ID
    if reply != None:
        quote_id = get_mapping(event.group_id, reply.message_id)
    else:
        quote_id = int(key) if key.isdigit() else None
        
    if quote_id == None:
        await mfinish(matcher_remove_quote, quote_not_found)
        return
    
    # 删除语录
    result = remove_quote(event.group_id, quote_id)
    if result:
        await mfinish(matcher_remove_quote, msg_remove_quote_success, author=get_group_member_cardname(event.group_id, event.sender.user_id or -1, bot))
    else:
        await mfinish(matcher_remove_quote, msg_remove_quote_failed)


comment_quote_alias = {"quote_comment", "评论语录", "评价语录", "评"}
matcher_comment_quote = on_command("评语录", aliases=comment_quote_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_comment_quote.handle()
@serial_execution
async def f_comment_quote(event: GroupME, bot: Bot, arg: Message = CommandArg()):
    """
    评论语录

    语录评论方式：
    `(reply) /评语录 评价`
    """
    # 判断 reply
    reply = event.reply
    content = arg.extract_plain_text().strip()
    if reply == None or content == "":
        await mfinish(matcher_comment_quote, msg_comment_quote_reply_args_missing)
        return

    # 获取语录 ID
    quote_id = get_mapping(event.group_id, reply.message_id)
    if quote_id == None:
        await mfinish(matcher_comment_quote, quote_not_found)
        return
    
    # 添加评论
    result = add_comment(event.group_id, quote_id, QuoteV2Comment(
        content=content,
        author_id=event.sender.user_id or -1,
        author_name=await get_group_member_cardname(event.group_id, event.sender.user_id or -1, bot) or event.sender.nickname or "",
        time_stamp=event.time,
    ))

    if result:
        await mfinish(matcher_comment_quote, msg_comment_quote_success)
    else:
        await mfinish(matcher_comment_quote, msg_comment_quote_failed)
