"""
语录管理器
"""
from ..imports import *
from dataclasses import dataclass, asdict

# Quote Data Class
VERSION_V1 = "1.0"
VERSION_V2 = "2.0"

@dataclass
class QuoteInfoV1:
    from_id: int
    from_name: str
    time_stamp: Optional[int]
    quote: str
    reason: str = ""
    show_time: int = 0
    ext_data: Optional[Dict] = None

@dataclass
class QuoteInfoV2:
    quote_id: int # 语录 ID，通常为被收录的消息 ID
    author_id: int # 作者 ID
    author_name: str # 作者名称
    author_card: str # 群名片
    time_stamp: Optional[int] # 时间戳
    quote: str # 语录内容
    reason: str = "" # 收录原因（评论）
    show_time: int = 0 # 展示次数
    recommend: bool = False # 推荐
    ext_data: Optional[Dict] = None

class QuoteManager:
    """
    语录管理器
    """
    def __init__(self, file_name: str):
        self.quote_list = []
        self.file_manager = JsonIO.from_module(PluginMetadata.name, "quotes")
        self.file_name = file_name
        
    def add_quote(self, quote: Union[QuoteInfoV1, QuoteInfoV2]):
        """添加语录到语录列表"""
        dict_quote = asdict(quote)
        
        if isinstance(quote, QuoteInfoV1):
            dict_quote["quote_id"] = hash(str(dict_quote["from_id"]) + dict_quote["quote"] + str(dict_quote["time_stamp"]))
            dict_quote["author_id"] = dict_quote["from_id"]
            dict_quote["author_name"] = dict_quote["from_name"]
            dict_quote["author_card"] = dict_quote["from_name"]
            dict_quote["time_stamp"] = dict_quote["time_stamp"]
            dict_quote["quote"] = dict_quote["quote"]
            dict_quote["reason"] = dict_quote["reason"]
            dict_quote["show_time"] = dict_quote["show_time"]
            dict_quote["recommend"] = False
            dict_quote["ext_data"] = dict_quote["ext_data"]
        
        self.quote_list.append(dict_quote)

    def update_show_time(self, quote_id: int, show_time: Optional[int] = None):
        """
        更新语录展示次数
        
        `quote_id`: 语录 ID
        `show_time`: 展示次数，如为 `None` 则加 1
        """
        for quote in self.quote_list:
            if quote["quote_id"] == quote_id:
                if show_time is None:
                    quote["show_time"] += 1
                else:
                    quote["show_time"] = show_time
                break

    def get_quotes(self):
        """获取所有语录"""
        return self.quote_list
    
    def get_typed_quotes(self):
        """
        获取所有语录 (typed)

        注意，由于是右值，如需更改需要手动重新进行 set_quotes
        """
        return [QuoteInfoV2(**quote) for quote in self.quote_list]
    
    def set_quotes(self, quotes: Union[List[QuoteInfoV2], List[Dict]]):
        """
        设置语录列表
        """
        if not quotes:
            self.quote_list = []

        if isinstance(quotes[0], QuoteInfoV2):
            self.quote_list: List = [asdict(quote) for quote in quotes] # type: ignore
        elif isinstance(quotes[0], dict):
            self.quote_list: List = quotes

    def load_from_file(self):
        """从文件加载语录"""
        default_data = {
            "version": VERSION_V2,
            "quote_list": []
        }
        data = self.file_manager.read_json(self.file_name, new_create=True, default_json=default_data)

        # 转换为 V2 格式
        if get_json_ver_info(data, VERSION_V1) == VERSION_V1:
            data = {"quote_list": data}
            data = set_json_ver_info(data, VERSION_V2)

        self.quote_list = data.get("quote_list", [])

    def save_to_file(self):
        """保存语录到文件"""
        data = {
            "version": VERSION_V2,
            "quote_list": self.quote_list
        }
        self.file_manager.save_json_atomic(self.file_name, data)

    def __enter__(self):
        self.load_from_file()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_to_file()
