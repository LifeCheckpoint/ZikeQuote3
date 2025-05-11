from typing import Optional, Dict, List, Tuple, Union

def msg_no_permission(event: Optional[str] = None):
    """没有权限"""
    if event == None:
        return {
            "ヾ(≧へ≦)〃嗯，要主人来才可以用这个功能哦~": 1,
        }
    else:
        return {
            f"ヾ(≧へ≦)〃嗯，要主人来才可以用「{event}」哦~": 1
        }

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

def msg_quote_not_found(key: Optional[str] = None):
    """语录未找到"""
    if key == None or key == "":
        return {
            "呜呜(っ﹏<。) 没有找到相关的语录呢...": 1,
            "查询失败...没找到相关的语录哦？": 1,
            "坏消息！没有找到符合条件的语录哦ヾ(≧へ≦)〃": 1,
            "抱歉，没找到符合条件的语录呢X﹏X": 1,
        }
    else:
        return {
            f"抱歉，没找到包含「{key}」的语录呢X﹏X": 1,
            f"呜呜(っ﹏<。) 没有找到包含「{key}」的语录呢...": 1,
            f"查询失败...没找到包含「{key}」的语录哦？": 1,
            f"坏消息！没有找到符合条件「{key}」的语录哦ヾ(≧へ≦)〃": 1,
        }
    
def msg_quote_on_update():
    """语录更新中"""
    return {
        "正在尝试更新语录...": 1,
        "正在更新语录o(*≧▽≦)ツ┏━┓": 1,
        "(∪.∪ )...zzz语录更新中！": 1,
    }

def msg_quote_update_success():
    """语录更新成功"""
    return {
        "语录更新成功啦！(≧∇≦)/": 1,
        "语录更新完成！(o゜▽゜)o☆": 1,
    }

def msg_quote_update_failed(error: Optional[str] = None):
    """语录更新失败"""
    return [{
        f"语录更新失败(っ °Д °;)っ...": 1,
        f"语录更新失败了呢o(TヘTo)...": 1,
    }, error if error else ""]

def msg_add_quote_reply_args_missing():
    """回复方式添加语录参数缺失"""
    return {
        "要回复一条文本消息哦⊙﹏⊙∥": 1,
        "要回复一条文本消息才能添加语录哦￣へ￣": 1,
        "这条回复里面什么都没说呢...": 1,
    }

def msg_add_quote_failed(error: Optional[str] = None):
    """添加语录失败"""
    reason = error or "我也不知道..."
    options = {
        f"Σ(っ °Д °;)っ 添加失败了... 原因：{reason}": 1,
        f"添加失败了呢... 服务器说：{reason} (╥﹏╥)": 1,
        f"糟糕！添加语录时遇到了问题：{reason} (⊙_⊙)": 1
    }
    return options

def msg_add_quote_success(author: Optional[str] = None):
    """添加语录成功"""
    options = {
        "语录添加成功啦！(≧∇≦)/": 1,
        "搞定！新的语录已经记下啦~ (ﾉ´ヮ´)ﾉ*:･ﾟ✧": 1,
        "添加成功！又多了一条可以回顾的记忆~ (*^▽^*)": 1
     } if not author else {
        f"添加成功！{author} 的语录已经记下啦~ (ﾉ´ヮ´)ﾉ*:･ﾟ✧": 1,
        f"搞定！{author} 的语录已经添加成功啦~ (≧∇≦)/": 1,
        f"好耶！{author} 的语录已经成功添加到我的记忆里了！(≧∇≦)/": 1
    }
    return options

def msg_remove_quote_reply_args_missing():
    """回复方式删除语录参数缺失"""
    return {
        "要回复一条语录哦(o゜▽゜)o☆": 1,
        "要回复一条语录消息才能删除语录哦~": 1,
    }

def msg_remove_quote_not_found():
    """删除语录未找到"""
    return {
        "没有找到对应的语录呢...可能太久远啦~": 1,
        "奇怪，没有找到对应的语录哦？(っ °Д °;)っ": 1,
        "没找到符合条件的语录呢~": 1,
    }

def msg_remove_quote_success(author: Optional[str]):
    """删除语录成功"""
    return {
        f"删除成功！{author} 的语录已经被删除啦~ (ﾉ´ヮ´)ﾉ*:･ﾟ✧": 1,
        f"搞定！{author} 的语录已经删除成功啦~ (≧∇≦)/": 1,
        f"好耶！{author} 的语录已经成功删除了！(≧∇≦)/": 1
    } if author != None else {
        "删除成功！语录已经被删除啦~ (ﾉ´ヮ´)ﾉ*:･ﾟ✧": 1,
        "搞定！语录已经删除成功啦~ (≧∇≦)/": 1,
        "好耶！语录已经成功删除了！(≧∇≦)/": 1
    }

def msg_remove_quote_failed(error: Optional[str] = None):
    """删除语录失败"""
    reason = error or "我也不知道..."
    options = {
        f"Σ(っ °Д °;)っ 删除失败了... 原因：{reason}": 1,
        f"删除失败了呢... 服务器说：{reason} (╥﹏╥)": 1,
        f"糟糕！删除语录时遇到了问题：{reason} (⊙_⊙)": 1
    }
    return options