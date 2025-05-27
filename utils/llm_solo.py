"""
LLM 调用相关函数
"""
from ..imports import *
from pathlib import Path
from openai import AsyncOpenAI

def get_openai_client(model_name: str) -> AsyncOpenAI:
    """
    获取 OpenAI 客户端实例
    """
    key_file = Path(__file__).parent / "api_key"

    if not key_file.exists():
        logger.warning(f"API 密钥文件 {key_file} 不存在，请创建并填入 API 密钥")
        key = None
    else:
        key = key_file.read_text().strip()

    return AsyncOpenAI(
        base_url=cfg.llm_base_url,
        api_key=key,
    )

async def llm_solo(content: str, attempt_num: int = 3) -> Optional[str]:
    """
    LLM 单次调用，使用 deepseek-chat，温度 0.2
    """
    client = get_openai_client("deepseek-chat")
    
    for attempt in range(attempt_num):
        try:
            response = await client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": content
                }],
                model="deepseek-chat",
                temperature=0.2,
                max_tokens=4000
            )
            chat_completion = response.choices[0].message.content

            if chat_completion == None or chat_completion.strip() == "":
                raise ValueError("LLM返回空")
        
            return chat_completion

        except Exception as e:
            print(f"API调用失败，第 {attempt+1} 次重试。错误信息：{str(e)}")
            await asyncio.sleep(2)
    
    return None