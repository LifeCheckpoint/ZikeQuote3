import asyncio
import functools

async_modify_lock = asyncio.Lock()

def serial_execution(func):
    """
    Decorator to ensure that an async function is executed serially.
    Only one instance of the decorated function can run at a time.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_modify_lock:
            result = await func(*args, **kwargs)
            return result

    return wrapper
