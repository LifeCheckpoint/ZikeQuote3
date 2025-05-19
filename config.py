from typing import List, Union
from pathlib import Path
from pydantic import BaseModel, Field

class PermissionConfig(BaseModel):
    """
    权限配置，控制哪些群组或用户可以使用语录功能
    """
    quote_managers: List[int] = Field(default=[], description="拥有管理语录权限的用户 ID 列表")

    mode_group: str = Field(default="white", description="群权限模式，可选值为 'white' (白名单) 或 'black' (黑名单)")
    white_group_list: List[int] = Field(default=[], description="白名单，允许使用语录功能的群组 ID 列表")
    black_group_list: List[int] = Field(default=[], description="黑名单，禁止使用语录功能的群组 ID 列表")

    mode_user: str = Field(default="black", description="用户权限模式，可选值为 'white' (白名单) 或 'black' (黑名单)")
    white_user_list: List[int] = Field(default=[], description="白名单，允许使用语录功能的用户 ID 列表")
    black_user_list: List[int] = Field(default=[], description="黑名单，禁止使用语录功能的用户 ID 列表")

    default_permission: Union[bool, str] = Field(default='user', description="默认权限模式，冲突时使用，'group' 为群权限优先，'user' 为用户权限优先，True 为一律允许，False 为一律禁止")

class PathConfig(BaseModel):
    """
    路径配置，定义插件相关文件的存储位置
    """
    root: Path = Field(default=Path(__file__).parent, description="插件的根目录")
    templates: Path = Field(default=Path(__file__).parent / "templates", description="存储语录模板文件的目录")
    prompts: Path = Field(default=Path(__file__).parent / "prompts", description="存储提示词文件的目录")

class Config(BaseModel):
    """
    ZikeQuote3 插件的全局配置
    """
    enable: bool = Field(default=True, description="是否启用 ZikeQuote3")
    enable_auto_collect: bool = Field(default=True, description="是否启用 LLM 自动收集群聊消息作为语录功能")
    enable_advanced_search: bool = Field(default=True, description="是否允许用户使用高级搜索语法查找语录")
    
    pickup_interval: int = Field(default=80, description="自动收集语录的间隔消息条数")
    msg_max_length: int = Field(default=35, description="允许被处理为语录的最大消息长度（字符数）")
    mapping_max_size: int = Field(default=50, description="内存中存储消息ID与语录ID映射关系的最大数量，用于避免重复收集")
    weight_p_transform: float = Field(default=1.2, description="语录权重幂变换的参数值越小，权重分布越平滑；值越大，高权重语录被选中的概率越高")
    enable_duplicate: bool = Field(default=False, description="是否允许同一个用户提交重复内容的语录")
    max_rank_show: int = Field(default=40, description="排行榜命令最多显示的用户数量")
    quote_list_num_perpage: int = Field(default=20, description="语录列表命令每页显示的语录数量")
    quote_list_page_limit: int = Field(default=4, description="语录列表命令允许显示的最大页数，超出此页数将不再显示之前的页码")
    quote_list_show_comment: int = Field(default=1, description="语录列表显示评论的模式\n0: 不显示评论；1: 显示最新一条非自动生成的评论；2: 显示最新一条评论（包括自动生成）")
    hitokoto_url: str = Field(default="https://v1.hitokoto.cn/", description="用于获取名人名言的 Hitokoto API 地址")

    path: PathConfig = Field(default_factory=PathConfig, description="路径配置")
    permission: PermissionConfig = Field(default_factory=PermissionConfig, description="权限配置")
