from ..imports import *
from .quote_type import QuoteManager, QuoteInfoV2, QuoteV2Comment, ID_AI
from ..utils.colors import generate_color_palette

def get_quote_file(group_id: int) -> str:
    """根据群组 ID 获取语录文件名"""
    return f"{group_id}.json"

def add_quote(group_id: int, quote: QuoteInfoV2):
    """
    添加语录到指定群组的语录文件中
    """
    quote_manager = QuoteManager(get_quote_file(group_id))
    with quote_manager:
        quote_manager.add_quote(quote)

def add_comment(group_id: int, quote_id: int, comment: QuoteV2Comment) -> bool:
    """
    添加评论到指定语录
    """
    quote_manager = QuoteManager(get_quote_file(group_id))
    with quote_manager:
        success = quote_manager.add_comment(quote_id, comment)
    return success

def remove_quote(group_id: int, quote_id: int) -> bool:
    """
    删除指定群组的语录
    """
    success = False
    quote_manager = QuoteManager(get_quote_file(group_id))
    with quote_manager:
        quotes = quote_manager.get_quotes()
        for quote in quotes:
            if quote["quote_id"] == quote_id:
                quotes.remove(quote)
                success = True
                break
        quote_manager.set_quotes(quotes)
    return success

def calculate_weight(quotes: List[QuoteInfoV2], filter: Callable[[QuoteInfoV2], bool] = lambda quote: True) -> Dict[int, float]:
    """
    计算语录的选取权重

    `return`: {quote_id: weight}
    """
    if not quotes:
        return {}
    
    filtered_quotes = [quote for quote in quotes if filter(quote)]
    if not filtered_quotes:
        return {}
    
    # 按照概率选择语录，出现次数越多的语录，概率越低，概率反比于出现次数
    # 通过幂变换平滑 / 增加权重差异
    # 同时出现次数要减去最低出现次数以防止最后 weight 趋于平均

    weights = {}
    min_show_time = abs(min(quote.show_time for quote in filtered_quotes))
    for quote in filtered_quotes:
        weights[quote.quote_id] = (1 / (quote.show_time - min_show_time + 1)) ** cfg.weight_p_transform
    
    total_weight = sum(weights.values())
    for id, weight in weights.items():
        weights[id] = weight / total_weight

    return weights

def get_typed_quote_list(group_id: int, filter: Callable[[QuoteInfoV2], bool] = lambda quote: True) -> List[QuoteInfoV2]:
    """
    获取语录列表 (typed)
    """
    quote_manager = QuoteManager(get_quote_file(group_id))
    quote_manager.load_from_file()
    quotes = quote_manager.get_typed_quotes()
    return [quote for quote in quotes if filter(quote)]

def get_random_quote(
        group_id: int,
        filter: Callable[[QuoteInfoV2], bool] = lambda quote: True,
        list_num: Optional[int] = None,
        update_showtime: bool = True,
    ) -> Optional[Union[QuoteInfoV2, List[QuoteInfoV2]]]:
    """
    随机获取语录

    `group_id`: 群组 ID
    `filter`: 过滤函数，返回 True 的语录会被选中
    `list_num`: 随机获取的语录数量，默认 None 表示选取一条并返回单独的语录对象，否则返回列表
    `update_showtime`: 是否更新语录展示次数，默认 True
    `transform_comments_type`: 是否转换评论类型到字典，默认 True
    """
    quotes = get_typed_quote_list(group_id, filter)
    if not quotes:
        return None
    
    weights = calculate_weight(quotes, filter)
    if not weights:
        return None
    
    if list_num is not None and list_num > len(quotes):
        list_num = len(quotes)

    if list_num is not None and list_num < 1:
        return None
    
    # 选择随机语录
    if list_num is None:
        result = random.choices(quotes, weights=list(weights.values()), k=1)[0]
    else:
        result = random.choices(quotes, weights=list(weights.values()), k=list_num)

    # 更新语录展示次数
    if update_showtime:
        qm = QuoteManager(get_quote_file(group_id))
        with qm:
            if isinstance(result, QuoteInfoV2):
                qm.update_show_time(result.quote_id)
            else:
                for quote in result: qm.update_show_time(quote.quote_id)

    return result

def get_quote_rank(group_id: int, filter: Callable[[QuoteInfoV2], bool] = lambda quote: True, top_n: int = cfg.max_rank_show) -> Dict[str, Any]:
    """
    获取语录排行

    `group_id`: 群组 ID
    `filter`: 过滤函数，返回 True 的语录会被选中
    """
    quote_list = get_typed_quote_list(group_id, filter)

    # 统计聊天语录基本信息
    current_quote_num = len(quote_list)
    author_ids = set(quote.author_id for quote in quote_list)
    author_num = len(author_ids)
    avg_quote_per_user = current_quote_num / author_num if author_num > 0 else 0

    # 统计语录作者语录个数
    author_quote_count = {}
    for quote in quote_list:
        if quote.author_id not in author_quote_count:
            author_quote_count[quote.author_id] = 0
        author_quote_count[quote.author_id] += 1
    sorted_quote_count = sorted(author_quote_count.items(), key=lambda x: x[1], reverse=True)
    top_quote_count = sorted_quote_count[:top_n]

    # 通过与最多语录的用户进行比较计算百分占比
    top_quote_info = []
    if len(top_quote_count) > 0:
        top1_quote_num = top_quote_count[0][1]
        for author_id, count in top_quote_count:
            author_card = next((quote.author_card for quote in quote_list if quote.author_id == author_id), None)
            top_quote_info.append({
                "author": author_card,
                "count": count,
                "percentage": f"{(count / top1_quote_num * 100):.2f}"
            })

    # 返回排行
    return {
        "group_name": group_id,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "stats": {
            "total_quotes": current_quote_num,
            "contributors": author_num,
            "average_quotes": f"{avg_quote_per_user:.2f}"
        },
        "ranking": top_quote_info
    }

def get_formatted_quote_list(quotes: List[QuoteInfoV2]) -> Dict[str, Any]:
    """
    获取格式化的分页语录列表，适用于基本的列表模板

    最终返回字段仅含有 `sections`，其余附加数据需要合并到最顶层字典

    `quotes`: 语录列表
    """
    total_page = (len(quotes) - 1) // cfg.quote_list_num_perpage + 1
    
    # 生成配色调色板
    colors = generate_color_palette(total_page)

    # 生成分页列表
    sections = []
    for i in range(total_page):

        page_quotes = quotes[i * cfg.quote_list_num_perpage: (i + 1) * cfg.quote_list_num_perpage]
        page_msg_txt = f"第 {i + 1} 页 / Page {i + 1}"

        boxes = []
        for j, quote in enumerate(page_quotes):
            # 根据评论显示模式判断是否需要显示
            match cfg.quote_list_show_comment:
                case 0:
                    is_comment_show = False
                case 1:
                    is_comment_show = quote.comments != [] and quote.comments[-1].author_id != ID_AI
                case 2:
                    is_comment_show = quote.comments != []
                case _:
                    print(f"未知的评论显示模式：{cfg.quote_list_show_comment}")
                    is_comment_show = False
            
            if is_comment_show:
                boxes.append({
                        "quote": f"{i * cfg.quote_list_num_perpage + j + 1}. {quote.quote}",
                        "comment": f"{quote.comments[-1].content}",
                        "comment_author_name": f"{quote.comments[-1].author_name}",
                    })
            else:
                boxes.append({
                    "quote": f"{i * cfg.quote_list_num_perpage + j + 1}. {quote.quote}",
                })

        sections.append({
            "title": page_msg_txt,
            "color": colors[i],
            "boxes": boxes
        })

    # 保留至多 cfg.quote_list_page_limit 页
    if len(sections) > cfg.quote_list_page_limit:
        sections = sections[-cfg.quote_list_page_limit:]
    
    # 生成数据
    return {"sections": sections}