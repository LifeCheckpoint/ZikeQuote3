from ..imports import *
from .quote_type import QuoteInfoV2, QuoteManager
from .llm_solo import llm_solo

def get_msg_file_name(group_id: int) -> str:
    """根据群组 ID 获取消息记录文件名"""
    return f"{group_id}.json"

def get_quote_file(group_id: int) -> str:
    """根据群组 ID 获取语录文件名"""
    return f"{group_id}.json"

def validate_msg(event: GroupME) -> bool:
    """验证事件中的消息是否符合一般收录条件"""
    message = event.get_plaintext().strip()
    if not message or message == "" or len(message) > cfg.msg_max_length:
        return False
    return True

async def get_group_member_cardname(group_id: int, user_id: int, bot: Bot) -> str:
    name = (await bot.get_group_member_info(group_id=group_id, user_id=user_id, no_cache=False)).get("card")
    return name if name else ""

async def pick_received_msg(event: GroupME, bot: Bot):
    if not validate_msg(event):
        return

    msg_id = event.message_id
    group_id = event.group_id
    group_name = event.get_session_id()
    user_id = event.user_id
    user_group_nickname = await get_group_member_cardname(group_id, user_id, bot)
    user_name = event.sender.nickname or ""
    time_stamp = event.time

    msg_file_name = get_msg_file_name(group_id)

    # 更新群组消息记录文件，完成后保存
    chat = ChatHistoryManager("quote_v3", "history", msg_file_name)
    with chat:
        chat.add_message(ChatMessageV3(
            message_id=msg_id,
            source_group_id=group_id,
            source_group_name=group_name,
            source_user_id=user_id,
            source_user_name=user_name,
            source_user_nickname=user_group_nickname,
            time_stamp=time_stamp,
            message=event.get_plaintext().strip()
        ))

        # 到达条数，触发更新并尝试清空
        if len(chat.get_messages()) >= cfg.pickup_interval:
            if await LLM_quote_pickup(group_id, chat.get_typed_messages()):
                chat.clear_messages()
            else:
                chat.clip_messages(cfg.pickup_interval - 1)

async def LLM_quote_pickup(group_id: int, message_list: List[ChatMessageV3]) -> bool:
    """调用 LLM 进行语录筛选提取"""
    prompt_quote_pickup = (cfg.path.prompts / "quote_pickup.txt").read_text(encoding="utf-8")
    full_prompt = template(prompt_quote_pickup, {
        "message_history": "\n".join([f"({msg.message_id}) {msg.source_user_name}: {msg.message}" for msg in message_list])
    })

    try:
        result = await llm_solo(full_prompt)
        if result == None: raise ValueError("空值被返回")
    except Exception as e:
        print("LLM 筛选语录失败，错误信息：", e)
        return False
    
    # 解析语录
    try:
        result = json.loads(result)
        if not isinstance(result, dict) or "num_quotes" not in result or "quotes" not in result:
            raise ValueError("解析响应失败，请检查响应：", result)
    except Exception as e:
        print("解析 LLM 返回语录失败，错误信息：", e)
        return False
    
    print(f"收集到 {result['num_quotes']} 条语录")
    for quote in result["quotes"]:
        # 获取 id
        target_quote_id = quote["id"]

        # 根据 id 查找消息
        message_data = next((msg for msg in message_list if str(msg.message_id) == str(target_quote_id)), None)
        if message_data is None:
            print(f"[Warning] 消息数据未找到: {target_quote_id}")
            continue

        # 添加语录
        qm = QuoteManager(get_quote_file(group_id))
        with qm:
            qm.add_quote(QuoteInfoV2(
                quote_id=target_quote_id,
                author_id=message_data.source_user_id,
                author_name=message_data.source_user_name,
                author_card=message_data.source_user_nickname,
                time_stamp=message_data.time_stamp,
                quote=quote["quote"],
                reason=quote["reason"],
                show_time=0,
                recommend=False,
                ext_data=None
            ))

    return True