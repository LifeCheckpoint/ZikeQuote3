"""
聊天记录管理器
"""
from .json_io import JsonIO
from .utils import get_json_ver_info, set_json_ver_info
from typing import Optional, Dict, Union, List
from dataclasses import dataclass, asdict
from pathlib import Path

# Message Data Class
VERSION_V1 = "1.0"
VERSION_V2 = "2.0"
VERSION_V3 = "3.0"

@dataclass
class ChatMessageV1:
    source_group_id: Optional[int]
    source_group_name: Optional[str]
    source_user_id: int
    source_user_name: str
    time_stamp: Optional[int]
    message: str
    ext_data: Optional[Dict] = None

@dataclass
class ChatMessageV2:
    source_group_id: Optional[int]
    source_group_name: Optional[str]
    source_user_id: int
    source_user_name: str
    source_user_nickname: str
    time_stamp: Optional[int]
    message: str
    ext_data: Optional[Dict] = None

@dataclass
class ChatMessageV3:
    message_id: int
    source_group_id: Optional[int]
    source_group_name: Optional[str]
    source_user_id: int
    source_user_name: str
    source_user_nickname: str
    time_stamp: Optional[int]
    message: str
    ext_data: Optional[Dict] = None

# Manager

class ChatHistoryManager:
    """
    聊天记录管理器
    """
    def __init__(self, plugin_name: str, module_name: Optional[str], file_name: str):
        self.message_list = []
        self.counter = 0
        self.file_manager = JsonIO.from_module(plugin_name, module_name)
        self.file_name = file_name

    def add_message(self, message: Union[ChatMessageV1, ChatMessageV2, ChatMessageV3]):
        """添加消息到消息列表"""
        dict_msg = asdict(message)

        if isinstance(message, ChatMessageV1):
            dict_msg["source_user_nickname"] = message.source_user_name
        if isinstance(message, ChatMessageV2):
            dict_msg["message_id"] = hash(message.message + str(message.time_stamp)) % 100000000
        self.message_list.append(dict_msg)
        self.counter += 1

    def set_counter(self, counter: int):
        """设置消息计数器"""
        self.counter = counter
        self.save_to_file()

    def get_messages(self) -> List[Dict]:
        """获取所有消息"""
        return self.message_list
    
    def get_typed_messages(self) -> List[ChatMessageV3]:
        """
        获取所有消息 (Typed)
        
        注意，由于是右值，如需更改需要手动重新进行 set_messages
        """
        return [ChatMessageV3(**msg) for msg in self.message_list]
    
    def set_messages(self, messages: Union[List[ChatMessageV3], List[Dict]]):
        """
        设置消息列表
        """
        if not messages:
            self.message_list = []

        if isinstance(messages[0], ChatMessageV3):
            self.message_list: List = [asdict(msg) for msg in messages] # type: ignore
        else:
            self.message_list: List = messages

    def clear_messages(self):
        """清空消息列表"""
        self.message_list.clear()

    def clip_messages(self, max_count: int):
        """裁剪消息列表到指定数量"""
        if len(self.message_list) > max_count:
            self.message_list = self.message_list[-max_count:]

    def load_from_file(self):
        """从文件加载消息记录"""
        default_data = {
            "version": VERSION_V3,
            "counter": 0,
            "chats": [],
        }
        data = self.file_manager.read_json(self.file_name, new_create=True, default_json=default_data)

        # 转换为 V2 格式
        if get_json_ver_info(data, VERSION_V1) == VERSION_V1:
            data = {"chats": data}
            data = set_json_ver_info(data, VERSION_V2)

        # 转换为 V3 格式
        chats = data.get("chats", [])
        if get_json_ver_info(data, VERSION_V2) == VERSION_V2:
            data = set_json_ver_info(data, VERSION_V3)
            for msg in chats:
                msg["message_id"] = hash(msg["message"] + str(msg["time_stamp"]))
                msg["source_user_nickname"] = msg["source_user_name"]

        if get_json_ver_info(data, VERSION_V3) == VERSION_V3:
            self.message_list = chats
            self.counter = int(data.get("counter", 0))
    
    def save_to_file(self):
        """保存消息记录到文件"""
        data = {
            "version": VERSION_V3,
            "counter": self.counter,
            "chats": self.message_list,
        }
        self.file_manager.save_json_atomic(self.file_name, data)

    def __enter__(self):
        self.load_from_file()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_to_file()
