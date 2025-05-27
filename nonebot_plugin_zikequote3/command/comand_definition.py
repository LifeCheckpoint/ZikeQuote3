from ..imports import on_message, on_command, quote_permission


# info_quote
matcher_listener = on_message(
    priority=15, block=False, permission=quote_permission
)

_rank_cmds = ("语录rank", "语录排行", "quote_rank", "语录信息", "quote_info")
matcher_rank = on_command(
    _rank_cmds[0],
    aliases=set(_rank_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_setting_showing_cmds = ("语录设置", "语录设置信息", "quote_setting", "语录配置", "quote_config", "查看语录设置", "查看语录配置")
matcher_setting_showing = on_command(
    _setting_showing_cmds[0],
    aliases=set(_setting_showing_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)


# modify_quote
_update_quote_cmds = ("语录强制更新", "更新语录", "语录更新", "强制更新语录", "强制语录更新")
matcher_update_quote = on_command(
    _update_quote_cmds[0],
    aliases=set(_update_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_add_quote_cmds = ("加语录", "add_quote", "quote_add", "添加语录", "新增语录", "语录添加")
matcher_add_quote = on_command(
    _add_quote_cmds[0],
    aliases=set(_add_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_remove_quote_cmds = ("删语录", "remove_quote", "quote_remove", "删除语录", "语录删除")
matcher_remove_quote = on_command(
    _remove_quote_cmds[0],
    aliases=set(_remove_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_comment_quote_cmds = ("评语录", "quote_comment", "评论语录", "评价语录", "评")
matcher_comment_quote = on_command(
    _comment_quote_cmds[0],
    aliases=set(_comment_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_del_comment_cmds = ("删评论", "del_comment", "删除评论", "删除语录评论", "删除语录评价")
matcher_del_comment = on_command(
    _del_comment_cmds[0],
    aliases=set(_del_comment_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)


# old_quote
_old_quote_cmds = ("老语录", "lt语录", "lt_quote", "老语录", "oldquote", "旧语录", "LT语录")
matcher_old_quote = on_command(
    _old_quote_cmds[0],
    aliases=set(_old_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)


# read_quote
_random_quote_cmds = ("语录", "quote", "随机语录")
matcher_random_quote = on_command(
    _random_quote_cmds[0],
    aliases=set(_random_quote_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_quote_card_cmds = ("语录卡", "语录图", "quote_card", "语录card", "语录图片")
matcher_quote_card = on_command(
    _quote_card_cmds[0],
    aliases=set(_quote_card_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_quote_list_cmds = ("语录列表", "语录list", "语录列表", "quote_list", "列语录")
matcher_quote_list = on_command(
    _quote_list_cmds[0],
    aliases=set(_quote_list_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)

_quote_search_cmds = ("查语录", "quote_search", "语录搜索", "语录查找", "搜语录", "找语录")
matcher_quote_search = on_command(
    _quote_search_cmds[0],
    aliases=set(_quote_search_cmds[1:]),
    priority=10, block=True, permission=quote_permission
)
