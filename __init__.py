from .imports import *

__plugin_meta__ = PluginMetadata(
    name="ZikeQuote3",
    description="LLM 介入，功能丰富的群聊语录自动收集与管理插件，支持自动收集、后台管理、生成排行榜、展示等功能",
    usage="""
    详见帮助
    """,
    config=Config,
    extra={
        "author": "LifeCheckpoint",
        "version": "0.3.0",
    },
)

from .command import *