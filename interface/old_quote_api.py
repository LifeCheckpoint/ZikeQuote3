from nonebot import get_plugin_config
from typing import Tuple
import requests

from ..config import Config
old_quote_cfg = get_plugin_config(Config).old_quote_config

url_random_key = f"{old_quote_cfg.base_url}/get_random",
url_random_global = f"{old_quote_cfg.base_url}/get_global_random"

def get_random_from_key(key: str) -> str:
    """
    获取指定键的随机语录

    `return`: 语录内容
    """
    response = requests.get(f"{url_random_key}/{key}", timeout=old_quote_cfg.timeout)
    if response.status_code == 404:
        raise ValueError("未找到指定键的语录")
    
    data = response.json()
    return data["result"]


def get_global_random() -> Tuple[str, str]:
    """
    获取全局随机语录

    `return`: [作者, 语录内容]
    """
    response = requests.get(url_random_global, timeout=old_quote_cfg.timeout)
    response.raise_for_status()
    
    data = response.json()
    return data['from_key'], data['result']
