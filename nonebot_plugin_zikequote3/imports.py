from dataclasses import asdict
from datetime import datetime
from nonebot import on_command, on_message, get_plugin_config, require, get_driver, logger
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import GroupMessageEvent as GroupME, MessageSegment as MsgSeg, Bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from pathlib import Path
from typing import Optional, Union, Literal, Callable, Any, Dict, List, Tuple
import asyncio
import colorsys
import json
import random
import requests

from .interface.permission import quote_permission, is_quote_manager
from .utils.async_tools import serial_execution, async_modify_lock
from .external.html_render import full_render_html, template, full_render_markdown
from .external.json_data_manager import ChatHistoryManager, ChatMessageV3, JsonIO
from .external.json_data_manager.utils import get_json_ver_info, set_json_ver_info
from .external.msg_text import msend, mfinish

from .config import Config
cfg = get_plugin_config(Config)

from .message_text import *