from ..imports import *
from ..interface.message_handle import (
    pick_received_msg,
    get_typed_message_list,
)
from ..interface.quote_handle import get_quote_rank


matcher_listener = on_message(priority=15, block=False, permission=quote_permission)
@matcher_listener.handle()
async def f_listener(event: GroupME, bot: Bot):
    """
    监听群组消息，处理可能的语录收集
    """
    if not cfg.enable_auto_collect:
        return
    
    success = await pick_received_msg(event, bot)
    if success == False:
        print("自动语录收集失败，可能需要检查相关配置")


rank_alias = {"语录排行", "quote_rank", "语录信息", "quote_info"}
matcher_rank = on_command("语录rank", aliases=rank_alias, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_rank.handle()
async def f_rank(event: GroupME):
    """
    语录排行
    """
    key = event.get_plaintext().strip()
    num_topn = cfg.max_rank_show
    if key.isdigit() and 0 < int(key) <= cfg.max_rank_show:
        num_topn = int(key)
    
    msg_pending_num = len(get_typed_message_list(event.group_id))
    rank_info = get_quote_rank(event.group_id, top_n=num_topn)
    rank_info["stats"]["pending_quotes"] = msg_pending_num

    try:
        image_data = await full_render_html(cfg.path.templates / "rank.html", cfg.path.templates, data=rank_info, width=800, height=600)
    except Exception as e:
        print("生成语录排行失败：", e)
        await mfinish(matcher_rank, msg_rank_failed, error=str(e))

    await matcher_rank.finish(MsgSeg.image(image_data))