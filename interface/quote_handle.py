from ..imports import *
from .quote_type import QuoteManager, QuoteInfoV2

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

