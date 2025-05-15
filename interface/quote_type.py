"""
语录管理器
"""
from ..imports import *
from dataclasses import dataclass, asdict

# Quote Data Class
VERSION_V1 = "1.0"
VERSION_V2 = "2.0"
ID_AI = -1

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
class QuoteV2Comment:
    content: str # 评论内容
    author_id: int # 评论作者 ID
    author_name: str # 评论作者名称 
    comment_id: Optional[int] = -1 # 评论 ID
    time_stamp: Optional[int] = -1 # 评论时间戳
    ext_data: Optional[Dict] = None

@dataclass
class QuoteInfoV2:
    quote_id: int # 语录 ID，通常为被收录的消息 ID
    author_id: int # 作者 ID
    author_name: str # 作者名称
    author_card: str # 群名片
    time_stamp: Optional[int] # 时间戳
    quote: str # 语录内容
    comments: List[QuoteV2Comment] = [] # 收录原因（评论）
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
        # V1 语录转换为 V2
        if isinstance(quote, QuoteInfoV1):
            quote_latest = QuoteInfoV2(
                quote_id = hash(str(quote.from_id) + quote.quote + str(quote.time_stamp)),
                author_id = quote.from_id,
                author_name = quote.from_name,
                author_card = quote.from_name,
                time_stamp = quote.time_stamp,
                quote = quote.quote,
                comments = [QuoteV2Comment(
                    comment_id = hash(quote.reason + str(quote.time_stamp)),
                    content = quote.reason,
                    author_id = ID_AI,
                    author_name = "AI",
                    time_stamp = quote.time_stamp,
                )],
                show_time = quote.show_time,
                recommend = False,
                ext_data = quote.ext_data,
            )
        else:
            quote_latest = quote
        
        self.quote_list.append(asdict(quote_latest))

    def remove_quote(self, quote_id: int):
        """
        删除语录
        
        `quote_id`: 语录 ID
        """
        for quote in self.quote_list:
            if quote["quote_id"] == quote_id:
                self.quote_list.remove(quote)
                return True
        return False

    def add_comment(self, quote_id: int, comment: QuoteV2Comment) -> bool:
        """
        添加评论到语录
        
        `quote_id`: 语录 ID
        `comment`: 评论内容
        """
        if comment.comment_id == None or comment.comment_id == -1:
            comment.comment_id = hash(comment.content + str(comment.time_stamp))
        
        for quote in self.quote_list:
            if quote["quote_id"] == quote_id:
                quote["comments"].append(asdict(comment))
                return True
        return False
    
    def remove_comment(self, quote_id: int, comment_id: int) -> bool:
        """
        删除语录评论
        
        `quote_id`: 语录 ID
        `comment_id`: 评论 ID
        """
        for quote in self.quote_list:
            if quote["quote_id"] == quote_id:
                for comment in quote["comments"]:
                    if comment["comments_id"] == comment_id:
                        quote["comments"].remove(comment)
                        return True
        return False

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
            self.quote_list = []
            for quote_v1 in data:
                self.add_quote(QuoteInfoV1(**quote_v1))
        elif get_json_ver_info(data, VERSION_V1) == VERSION_V2:
            self.quote_list = data.get("quote_list", [])
        else:
            raise ValueError(f"不支持的语录版本: {data.get('version', 'Unknown')}")

    def save_to_file(self):
        """保存语录到文件"""
        data = {
            "version": VERSION_V2,
            "quote_list": self.quote_list
        }
        self.file_manager.save_json_atomic(self.file_name, data)

    def __enter__(self):
        """
        读取并保存语录上下文管理器
        """
        self.load_from_file()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_to_file()
