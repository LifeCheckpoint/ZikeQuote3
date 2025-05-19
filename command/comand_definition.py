from ..imports import on_message, on_command, quote_permission

# info_quote
matcher_listener = on_message(
    priority=15, block=False, permission=quote_permission
)
matcher_rank = on_command(
    ("语录rank", "语录排行", "quote_rank", "语录信息", "quote_info"),
    priority=10, block=True, permission=quote_permission
)
matcher_setting_showing = on_command(
    ("语录设置", "语录设置信息", "quote_setting", "语录配置", "quote_config", "查看语录设置", "查看语录配置"),
    priority=10, block=True, permission=quote_permission
)

# modify_quote
matcher_update_quote = on_command(
    ("语录强制更新", "更新语录", "语录更新", "强制更新语录", "强制语录更新"),
    priority=10, block=True, permission=quote_permission
)
matcher_add_quote = on_command(
    ("加语录", "add_quote", "quote_add", "添加语录", "新增语录", "语录添加"),
    priority=10, block=True, permission=quote_permission
)

matcher_remove_quote = on_command(
    ("删语录", "remove_quote", "quote_remove", "删除语录", "语录删除"),
    priority=10, block=True, permission=quote_permission
)
matcher_comment_quote = on_command(
    ("评语录", "quote_comment", "评论语录", "评价语录", "评"), 
    priority=10, block=True, permission=quote_permission
)
matcher_del_comment = on_command(
    ("删评论", "del_comment", "删除评论", "删除语录评论", "删除语录评价"), 
    priority=10, block=True, permission=quote_permission
)

# old_quote
matcher_old_quote = on_command(
    ("老语录", "lt语录", "lt_quote", "老语录", "oldquote", "旧语录", "LT语录"),
    priority=10, block=True, permission=quote_permission
)

# read_quote
matcher_random_quote = on_command(
    ("语录", "quote", "随机语录"), 
    priority=10, block=True, permission=quote_permission
)
matcher_quote_card = on_command(
    ("语录卡", "语录图", "quote_card", "语录card", "语录图片"), 
    priority=10, block=True, permission=quote_permission
)
matcher_quote_list = on_command(
    ("语录列表", "语录list", "语录列表", "quote_list", "列语录"),
    priority=10, block=True, permission=quote_permission
)
matcher_quote_search = on_command(
    ("查语录", "quote_search", "语录搜索", "语录查找", "搜语录", "找语录"),
    priority=10, block=True, permission=quote_permission
)
