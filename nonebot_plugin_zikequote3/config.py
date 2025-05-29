from typing import List, Union, Optional, Literal
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

class PermissionConfig(BaseModel):
    """
    权限配置，控制哪些群组或用户可以使用语录功能
    """
    quote_managers: List[int] = Field(default=[], description="拥有管理语录权限的用户 ID 列表")

    mode_group: Literal["white", "black"] = Field(default="white", description="群权限模式，可选值为 'white' (白名单) 或 'black' (黑名单)")
    white_group_list: List[int] = Field(default=[], description="白名单，允许使用语录功能的群组 ID 列表")
    black_group_list: List[int] = Field(default=[], description="黑名单，禁止使用语录功能的群组 ID 列表")

    mode_user: Literal["white", "black"] = Field(default="black", description="用户权限模式，可选值为 'white' (白名单) 或 'black' (黑名单)")
    white_user_list: List[int] = Field(default=[], description="白名单，允许使用语录功能的用户 ID 列表")
    black_user_list: List[int] = Field(default=[], description="黑名单，禁止使用语录功能的用户 ID 列表")

    default_permission: Union[bool, Literal["user", "group"]] = Field(default=False, description="默认权限模式，冲突时使用，'group' 为群权限优先，'user' 为用户权限优先，True 为一律允许，False 为一律禁止")

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

    check_frontend: bool = Field(default=True, description="自动检查并安装前端 Node.js 依赖（若未安装），配置为 False 则忽略检查，如果前端依赖未安装则无法使用包含图像生成的命令")
    
    pickup_interval: int = Field(default=80, description="自动收集语录的间隔消息条数，必须大于10")
    msg_max_length: int = Field(default=35, description="允许被处理为语录的最大消息长度（字符数），必须大于0")
    mapping_max_size: int = Field(default=50, description="内存中存储消息ID与语录ID映射关系的最大数量，必须大于等于1")
    weight_p_transform: float = Field(default=1.2, description="语录权重幂变换的参数值越小，权重分布越平滑；值越大，高权重语录被选中的概率越高，必须大于等于0且小于10")
    enable_duplicate: bool = Field(default=False, description="是否允许同一个用户提交重复内容的语录")
    max_rank_show: int = Field(default=40, description="排行榜命令最多显示的用户数量，必须大于等于1")
    quote_list_num_perpage: int = Field(default=20, description="语录列表命令每页显示的语录数量，必须大于等于1")
    quote_list_page_limit: int = Field(default=4, description="语录列表命令允许显示的最大页数，超出此页数将不再显示之前的页码，必须大于等于1")
    quote_list_show_comment: Literal[0, 1, 2] = Field(default=1, description="语录列表显示评论的模式\n0: 不显示评论；1: 显示最新一条非自动生成的评论；2: 显示最新一条评论（包括自动生成）")
    hitokoto_url: str = Field(default="https://v1.hitokoto.cn/", description="用于获取名人名言的 Hitokoto API 地址")
    llm_base_url: Optional[str] = Field(default=None, description="LLM API 的基础 URL，填写后可在 `llm_solo` 进行适配更改")

    path: PathConfig = Field(default_factory=PathConfig, description="路径配置")
    permission: PermissionConfig = Field(default_factory=PermissionConfig, description="权限配置")

    # 验证参数合法性
    @field_validator("path")
    @classmethod
    def validate_path(cls, v: PathConfig) -> PathConfig:
        """验证路径配置是否存在"""
        if not v.root.exists():
            raise ValueError(f"根目录不存在: {v.root}")
        if not v.templates.exists():
            raise ValueError(f"模板目录不存在: {v.templates}")
        if not v.prompts.exists():
            raise ValueError(f"提示词目录不存在: {v.prompts}")
        return v

    @field_validator("pickup_interval")
    @classmethod
    def validate_pickup_interval(cls, v: int) -> int:
        """验证pickup_interval必须大于10"""
        if v <= 10:
            raise ValueError("pickup_interval必须大于10")
        return v

    @field_validator("msg_max_length")
    @classmethod
    def validate_msg_max_length(cls, v: int) -> int:
        """验证msg_max_length必须大于0"""
        if v <= 0:
            raise ValueError("msg_max_length必须大于0")
        return v

    @field_validator("mapping_max_size")
    @classmethod
    def validate_mapping_max_size(cls, v: int) -> int:
        """验证mapping_max_size必须大于等于1"""
        if v < 1:
            raise ValueError("mapping_max_size必须大于等于1")
        return v

    @field_validator("weight_p_transform")
    @classmethod
    def validate_weight_p_transform(cls, v: float) -> float:
        """验证weight_p_transform必须大于等于0且小于10"""
        if v < 0 or v >= 10:
            raise ValueError("weight_p_transform必须大于0且小于10")
        return v

    @field_validator("max_rank_show")
    @classmethod
    def validate_max_rank_show(cls, v: int) -> int:
        """验证max_rank_show必须大于等于1"""
        if v < 1:
            raise ValueError("max_rank_show必须大于等于1")
        return v

    @field_validator("quote_list_num_perpage")
    @classmethod
    def validate_quote_list_num_perpage(cls, v: int) -> int:
        """验证quote_list_num_perpage必须大于等于1"""
        if v < 1:
            raise ValueError("quote_list_num_perpage必须大于等于1")
        return v

    @field_validator("quote_list_page_limit")
    @classmethod
    def validate_quote_list_page_limit(cls, v: int) -> int:
        """验证quote_list_page_limit必须大于等于1"""
        if v < 1:
            raise ValueError("quote_list_page_limit必须大于等于1")
        return v
