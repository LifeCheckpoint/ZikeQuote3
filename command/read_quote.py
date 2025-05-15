"""
语录显示相关命令
"""

from ..imports import *
from ..interface.message_handle import (
    add_mapping,
)
from ..interface.quote_handle import (
    QuoteInfoV2,
    get_random_quote,
    get_typed_quote_list,
    get_formatted_quote_list
)
from ..utils.hitokoto import get_hitokoto


random_quote_alias = {"quote", "随机语录"}
matcher_random_quote = on_command("语录", aliases=random_quote_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_random_quote.handle()
async def f_random_quote(event: GroupME, bot: Bot, arg: Message = CommandArg()):
    """
    随机语录
    """
    key = arg.extract_plain_text().strip() # 默认为搜索名字+内容
    if key == "":
        result: QuoteInfoV2 = get_random_quote(event.group_id) # type: ignore
    else:
        filt: Callable[[QuoteInfoV2], bool] = lambda quote: key in quote.quote or key in quote.author_name or key in quote.author_card
        result: QuoteInfoV2 = get_random_quote(event.group_id, filt) # type: ignore

    if not result:
        await mfinish(matcher_random_quote, msg_quote_not_found, key=key)
    else:
        send_msg = await msend(matcher_random_quote, msg_send_quote, author=result.author_name, quote=result.quote)
        add_mapping(event.group_id, send_msg["message_id"], result.quote_id)


quote_card_alias = {"语录图", "quote_card", "语录card", "语录图片"}
matcher_quote_card = on_command("语录卡", aliases=quote_card_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_quote_card.handle()
async def f_quote_card(event: GroupME, arg: Message = CommandArg()):
    """
    语录卡生成
    """
    key = arg.extract_plain_text().strip()
    if key == "":
        result: QuoteInfoV2 = get_random_quote(event.group_id) # type: ignore
    else:
        filt: Callable[[QuoteInfoV2], bool] = lambda quote: key in quote.quote or key in quote.author_name or key in quote.author_card
        result: QuoteInfoV2 = get_random_quote(event.group_id, filt) # type: ignore

    if not result:
        await mfinish(matcher_quote_card, msg_quote_not_found, key=key)
    else:
        # 生成图片
        try:
            image_data = await full_render_html(cfg.path.templates / "card.html", cfg.path.templates, data=asdict(result), width=630, height=120)
            send_msg = await matcher_quote_card.send(MsgSeg.image(image_data))
            add_mapping(event.group_id, send_msg["message_id"], result.quote_id)
        except Exception as e:
            print(f"生成语录卡失败：{e}")
            await mfinish(matcher_quote_card, msg_quote_card_failed, error=str(e))


quote_list_alias = {"语录list", "语录列表", "quote_list", "列语录"}
matcher_quote_list = on_command("语录列表", aliases=quote_list_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_quote_list.handle()
async def f_quote_list(event: GroupME, arg: Message = CommandArg()):
    """
    语录列表
    """
    key = arg.extract_plain_text().strip()
    # 默认以发送者 QQ 为关键词检索列表
    if key == "":
        key = event.sender.user_id

    # 精确匹配
    filt: Callable[[QuoteInfoV2], bool] = lambda quote: key == quote.author_name or key == quote.author_card or str(key) == str(quote.author_id)
    quotes = get_typed_quote_list(event.group_id, filter=filt)
    author_id_set = set(quote.author_id for quote in quotes)

    if not author_id_set:
        await mfinish(matcher_quote_list, msg_quote_list_not_found, key=key)

    if len(author_id_set) > 1:
        await mfinish(matcher_quote_list, msg_quote_list_ambiguous, key=key, num=len(author_id_set))

    # 获取用户所有格式化的语录列表
    data = get_formatted_quote_list(quotes)
    author = quotes[0].author_name if quotes else key

    time_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    author_stat = f"{len(quotes)} 条语录" + (f"（最新 {cfg.quote_list_page_limit} 页）" if len(quotes) > cfg.quote_list_num_perpage * cfg.quote_list_page_limit else "")
    addition_text = get_hitokoto()[0] or "桃李不言，下自成蹊"

    data = data | {
        "title": f"来自{author}的语录",
        "description": f"{time_text} / {author_stat}",
        "addition": addition_text,
    }

    # 生成图片
    try:
        image_data = await full_render_html(cfg.path.templates / "list.html", cfg.path.templates, data=data, width=800, height=200)
        await matcher_quote_list.send(MsgSeg.image(image_data))
    except Exception as e:
        print(f"生成语录列表失败：{e}")
        await mfinish(matcher_quote_list, msg_quote_list_generate_failed, error=str(e))


quote_search_alias = {"quote_search", "语录搜索", "语录查找", "搜语录", "找语录"}
matcher_quote_search = on_command("查语录", aliases=quote_search_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_quote_search.handle()
async def f_quote_search(event: GroupME, arg: Message = CommandArg()):
    """
    语录搜索
    """
    key = arg.extract_plain_text().strip()
    if key == "":
        await mfinish(matcher_quote_search, msg_quote_search_empty)

    # 精确匹配
    filt: Callable[[QuoteInfoV2], bool] = lambda quote: key in quote.quote
    quotes = get_typed_quote_list(event.group_id, filter=filt)

    if not quotes:
        await mfinish(matcher_quote_search, msg_quote_not_found, key=key)

    # 获取用户所有格式化的语录列表
    data = get_formatted_quote_list(quotes)

    time_text = datetime.now().strftime("%Y-%m-%d %H:%M")
    author_stat = f"{len(quotes)} 条搜索结果" + f"（最新 {cfg.quote_list_page_limit} 页）" if len(quotes) > cfg.quote_list_num_perpage * cfg.quote_list_page_limit else ""
    addition_text = get_hitokoto()[0] or "桃李不言，下自成蹊"

    data = data | {
        "title": f"包含{key}的语录",
        "description": f"{time_text} / {author_stat}",
        "addition": addition_text,
    }

    # 生成图片
    try:
        image_data = await full_render_html(cfg.path.templates / "list.html", cfg.path.templates, data=data, width=800, height=200)
        await matcher_quote_search.send(MsgSeg.image(image_data))
    except Exception as e:
        print(f"生成语录搜索列表失败：{e}")
        await mfinish(matcher_quote_search, msg_quote_list_generate_failed, error=str(e))
