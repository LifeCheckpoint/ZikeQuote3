from nonebot.adapters.onebot.v11 import GroupMessageEvent as GroupME
from nonebot import get_plugin_config

from ..config import Config
cfg = get_plugin_config(Config)

async def quote_permission(event: GroupME):
    """
    群权限管理，可用白名单或黑名单
    """
    match cfg.permission.mode:
        case "white":
            permission = str(event.group_id) in str(cfg.permission.white_list)
        case "black":
            permission = str(event.group_id) not in str(cfg.permission.black_list)
        case _:
            print("权限模式错误，请检查配置")
            permission = False
            
    return permission