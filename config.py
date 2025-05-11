from pathlib import Path
from pydantic import BaseModel

class OldQuoteConfig(BaseModel):
    """
    旧语录库配置
    """
    enable: bool = True # 是否启用旧语录库
    base_url: str = "http://artonelicfrequence.icu/"
    timeout: int = 5 # API 超时时间

class PermissionConfig(BaseModel):
    """
    权限配置
    """
    mode: str = "white" # 权限模式，white 或 black
    white_list: list[int] = [980606481, 732909252] # 白名单，允许的群组 ID 列表
    black_list: list[int] = [] # 黑名单，禁止的群组 ID 列表

class PathConfig(BaseModel):
    """
    路径配置
    """
    root: Path = Path(__file__).parent # 插件根目录
    templates: Path = root / "templates" # 模板目录
    prompts: Path = root / "prompts" # 提示词目录

class Config(BaseModel):
    """
    Quote V3 插件配置
    """
    enable: bool = False # 启用插件
    quote_managers: list[int] = [2435206827] # 管理员
    pickup_interval: int = 80 # 语录收集间隔
    msg_max_length: int = 35 # 允许被处理的最大消息长度
    mapping_max_size: int = 50 # 储存消息ID-语录ID映射的最大数量
    weight_p_transform: float = 1.2 # 权重幂变换参数，越小越平滑，越大越容易选到高权重语录
    enable_duplicate: bool = False # 是否允许个人语录重复收录

    path: PathConfig = PathConfig()
    permission: PermissionConfig = PermissionConfig()
    old_quote_config: OldQuoteConfig = OldQuoteConfig()