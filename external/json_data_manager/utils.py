"""
实用工具
"""
from typing import List, Dict, Any, Optional, Union
from .json_io import JsonIO

def get_json_ver_info(data: Union[Dict, Any], default: Optional[str] = None) -> Union[str, None]:
    """
    检查版本信息
    """
    if isinstance(data, Dict):
        return data.get("version", default)
    elif isinstance(data, List):
        return default
    else:
        return default

def set_json_ver_info(data: Dict, version: str) -> Dict:
    """
    设置版本信息
    """
    if not isinstance(data, Dict):
        raise ValueError("Data must be a dictionary")
    
    data["version"] = version
    return data