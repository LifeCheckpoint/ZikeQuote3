from typing import Optional, Dict, List, Tuple, Union

def msg_api_request_error(error: Optional[str] = None):
    """API 请求错误"""
    head = {
        "连接不上语录服务器了... 是不是网络坏掉了？": 1,
        "尝试连接服务器失败了... 网络连接正常吗？( T_T)": 1,
        "呜... 无法连接到语录服务器... 请稍后再试试吧 (＞﹏＜)": 1,
    }
    if error != None:
        return [head, "\n\n", "错误原因：", error]
    else:
        return [head]

def msg_send_quote(author: str, quote: str):
    """发送语录"""
    return {
        f"{author}曾经说过：{quote}": 1,
        f"{author}曰：{quote}": 1,
        f"{author}说：{quote}": 1,
        f"{author}：{quote}": 1,
        f"{quote}\n——{author}": 0.5,
    }
