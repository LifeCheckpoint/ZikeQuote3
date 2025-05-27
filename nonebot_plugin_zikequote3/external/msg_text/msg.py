import random as ran
from typing import List, Mapping, Callable, Union, Mapping, Any
from nonebot.matcher import Matcher

Number = Union[int, float]
ProbText = Mapping[str, Number]
SuppotedText = Union[str, ProbText]
SupportedTextCombined = Union[SuppotedText, List[SuppotedText]]

def select_string_list(strings: List[str], probabilities: List[Number]) -> str:
    """根据概率选择字符串"""
    if len(strings) != len(probabilities):
        raise ValueError("字符串列表和概率列表的长度不匹配")

    total_prob = sum(probabilities) # type: ignore
    if total_prob == 0:
        raise ValueError("概率列表的总和不能为0")

    normalized_probabilities = [p / total_prob for p in probabilities]

    selected = ran.choices(strings, weights=normalized_probabilities, k=1)
    return selected[0]

def select_string_map(strings: ProbText) -> str:
    """根据概率选择字符串"""
    return select_string_list(list(strings.keys()), list(strings.values()))

def mtxtf(text_func: Callable[..., Union[SupportedTextCombined, Any]], **kwargs) -> str:
    """
    通过调用函数发送指定的消息

    参数可以是固定字符串、概率字符串字典，或者由两者组合而成的列表拼接文本
    
    使用示例：
    ```
    # summary_success_output(summary: str, num_msg: int = None) -> List
    mtxtf(summary_success_output, summary="这是消息总结", num_msg=5)
    ```
    """
    probably_result = text_func(**kwargs)

    # 字符串，直接返回
    if isinstance(probably_result, str):
        return probably_result
    
    # 字典，代表单条概率消息
    if isinstance(probably_result, Mapping):
        return select_string_map(probably_result)

    # 列表，代表多条可能消息的拼接
    if isinstance(probably_result, List):
        result_text = ""
        for item in probably_result:
            # 纯字符串，直接拼接
            if isinstance(item, str):
                result_text += item
            # 字典，概率拼接
            elif isinstance(item, Mapping):
                result_text += select_string_map(item)
            else:
                raise ValueError("输出列表返回值必须是字典或字典列表")
        return result_text
    
    raise ValueError("输出返回值必须是字典或字典列表")

async def msend(matcher: type[Matcher], text_func: Callable[..., Union[SupportedTextCombined, Any]], **kwargs):
    """发送消息"""
    return await matcher.send(mtxtf(text_func, **kwargs))

async def mfinish(matcher: type[Matcher], text_func: Callable[..., Union[SupportedTextCombined, Any]], **kwargs):
    """结束消息"""
    await matcher.finish(mtxtf(text_func, **kwargs))