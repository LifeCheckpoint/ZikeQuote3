import json
import os
import tempfile
import nonebot_plugin_localstore as store
from pathlib import Path
from typing import Optional, Union, Any, overload, TYPE_CHECKING
from dataclasses import asdict

def default_serializer(obj):
    if hasattr(obj, "__dataclass_fields__"):  # 检查是否是 dataclass
        return asdict(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

class JsonIO:
    """
    管理插件的 Json 数据，支持原子写入和读取
    """
    if TYPE_CHECKING:
        plugin_name: str
        plugin_data_dir: Path
        single_file: str

    @staticmethod
    def from_module(plugin_name: str, module_name: Optional[str] = None):
        """
        管理插件 Json 数据文件

         - `plugin_name` 插件名称
         - `module_name` 模块名称，可以由路径构成
        """
        self = JsonIO()
        self.plugin_name = plugin_name
        if module_name is None:
            self.plugin_data_dir = store.get_data_dir(plugin_name)
        else:
            self.plugin_data_dir = store.get_data_dir(plugin_name) / module_name

        return self

    @staticmethod
    def from_file(file_name: Union[str, Path]):
        """
        管理单个 Json 数据文件

         - `file_name` 文件名称
        """
        self = JsonIO()
        self.single_file = str(file_name)

        return self

    def _get_file_path(self, file_name: Optional[str]) -> Path:
        if hasattr(self, 'single_file'):
            # 如果是单个文件，则直接返回文件路径
            return Path(self.single_file)
        else:
            if file_name is None:
                raise ValueError("file_name 不能为空")
            return self.plugin_data_dir / file_name
    
    def save_json_atomic(self, file_name: Optional[str], data):
        """
        使用原子写入方式保存 JSON 数据。
        """
        # 创建一个临时文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp_file:
            try:
                json.dump(data, tmp_file, indent=4, ensure_ascii=False, default=default_serializer)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())
            except Exception as e:
                print(f"写入临时文件时发生错误: {e}")
                os.remove(tmp_file.name)
                raise

        # 同步到目标文件
        try:
            file_path = self._get_file_path(file_name)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            os.replace(tmp_file.name, str(file_path))
        except Exception as e:
            print(f"重命名文件时发生错误: {e}")
            os.remove(tmp_file.name)
            raise
    
    def read_json(self, file_name: Optional[str] = None, new_create: bool = True, default_json: Any = {}):
        """读取 JSON 文件"""
        file_path = self._get_file_path(file_name)
        if not file_path.exists() and not new_create:
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        if not file_path.exists() and new_create:
            # 如果文件不存在，则创建一个空的 JSON 文件
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                print(f"文件创建 {file_path}")
                json.dump(default_json, f, indent=4, ensure_ascii=False)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
