from ..imports import *
from .comand_definition import *
from ..utils.old_quote_api import *


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