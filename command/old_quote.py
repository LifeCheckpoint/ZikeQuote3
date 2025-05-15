from ..imports import *
from ..utils.old_quote_api import *

old_quote_aliases = {"lt语录", "lt_quote", "老语录", "oldquote", "旧语录", "LT语录"}
matcher_old_quote = on_command("老语录", aliases=old_quote_aliases, priority=10, block=True, permission=quote_permission) # type: ignore
@matcher_old_quote.handle()
async def _(args: Message = CommandArg()):
    """
    老语录指令，随机指定人语录或全局随机语录
    """
    key = args.extract_plain_text().strip()

    try:
        if key:
            author, quote = key, get_random_from_key(key)
        else:
            author, quote = get_global_random()
    except Exception as e:
        await mfinish(matcher_old_quote, msg_api_request_error, error=str(e))

    await mfinish(matcher_old_quote, msg_send_quote, author=author, quote=quote)