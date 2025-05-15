"""
管理全局消息状态
"""
from .. import __plugin_meta__
from ..imports import *

class HistoryQuoteState:
    """
    通过消息机制，保存发出的消息与语录 ID 之间的关联，从而允许 reply 等场景下获取到对应语录 ID
    """
    def __init__(self, file_name: str):
        self.mapping_list = []
        self.file_manager = JsonIO.from_module(__plugin_meta__.name, "HistoryMapping")
        self.file_name = file_name
        self.load_from_file()

    def load_from_file(self):
        """从文件加载映射关系"""
        self.mapping_list = self.file_manager.read_json(self.file_name, new_create=True, default_json=[])

    def save_to_file(self):
        """保存映射关系到文件"""
        self.file_manager.save_json_atomic(self.file_name, self.mapping_list)

    def add_mapping(self, message_id: int, quote_id: int):
        """添加消息 ID 与语录 ID 的映射关系"""
        self.mapping_list.append({
            "message_id": message_id,
            "quote_id": quote_id
        })
        self.save_to_file()
        self.clip_mapping()

    def get_mapping(self, message_id: int) -> Optional[int]:
        """获取消息 ID 对应的语录 ID"""
        for mapping in self.mapping_list:
            if mapping["message_id"] == message_id:
                return mapping["quote_id"]
        return None

    def clip_mapping(self, max_size: int = cfg.mapping_max_size):
        """保留映射最大数量为 max_size"""
        if len(self.mapping_list) > max_size:
            self.mapping_list = self.mapping_list[-max_size:]
            self.save_to_file()