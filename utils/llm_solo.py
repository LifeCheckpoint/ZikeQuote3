"""
LLM 调用相关函数
"""
from ..imports import *

def get_openai_client(model: str):
    pass

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