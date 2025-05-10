from ..imports import *
from ..interface.old_quote_api import *

match_quote_aliases = {"lt语录", "lt_quote", "老语录", "oldquote", "旧语录", "LT语录"}
matcher_old_quote = on_command("老语录", aliases=match_quote_aliases, priority=10, block=True, permission=quote_permission)
@matcher_old_quote.handle()
async def _(args: Message = CommandArg()):
    """
    老语录指令，随机指定人语录或全局随机语录
    """
    key = args.extract_plain_text().strip()
    result = {}

    try:
        if key:
            result["from_name"], result["quote"] = key, get_random_from_key(key)
        else:
            result["from_name"], result["quote"] = get_global_random()
    except Exception as e:
        await mfinish(matcher_old_quote, msg_api_request_error, error=str(e))

    await mfinish(matcher_old_quote, msg_send_quote, author=result["author"], quote=result["quote"])