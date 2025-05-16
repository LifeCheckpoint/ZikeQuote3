"""
对网页进行截图
"""
import asyncio
import subprocess
from typing import Tuple, Union
from pathlib import Path

NODE_SCRIPT_PATH = Path(__file__).parent / 'screenshot.js'

async def async_generate_screenshot(
        html_file: Path,
        save_name: Path,
        width: int = 1000,
        height: int = 800,
        device_scale_factor: float = 2.0
    ) -> Tuple[int, str, str]:
    """
    异步生成网页截图。

    Args:
        html_file (str): HTML 文件绝对路径。
        save_name (str): 截图保存文件绝对路径。
        width (int): 视口宽度。
        height (int): 视口高度。
        device_scale_factor (float): 设备缩放因子。

    Returns:
        tuple: 包含 (返回码, 标准输出, 标准错误) 的元组。
               返回码是 Node.js 进程的退出码。
               标准输出和标准错误是捕获到的字符串。
    """

    command = [
        'node',
        str(NODE_SCRIPT_PATH),
        str(save_name.absolute()),
        str(html_file.absolute()),
        str(width),
        str(height),
        str(device_scale_factor)
    ]

    try:
        # 异步创建子进程
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # print(f"已启动截图进程 (PID: {process.pid})...")

        # 异步等待进程完成并读取输出
        stdout, stderr = await process.communicate()

        stdout_str = stdout.decode('utf-8').strip()
        stderr_str = stderr.decode('utf-8').strip()

        # print(f"截图进程 (PID: {process.pid}) 已完成，返回码: {process.returncode}")

        if process.returncode == 0:
            print("截图生成成功")
            # if stdout_str:
            #     print("Node.js 标准输出:", stdout_str)
        else:
            print(f"截图生成失败 (返回码: {process.returncode})")
            if stderr_str:
                print("Node.js 错误:", stderr_str)

        return process.returncode, stdout_str, stderr_str

    except FileNotFoundError:
        print("截图错误: 未找到 node 或 screenshot.js。请确保它们在系统路径中或脚本路径正确。")
        return -1, "", "错误: 未找到 node 或 screenshot.js。"
    except Exception as e:
        print(f"截图错误: {e}")
        return -2, "", str(e)

# 示例如何运行这个异步函数
async def main():
    print("正在启动异步截图任务...")

    # 并发运行多个截图任务
    task1 = asyncio.create_task(async_generate_screenshot('my_page.html', 'async_screenshot1.png', width=1200))
    task2 = asyncio.create_task(async_generate_screenshot('another_page.html', 'async_screenshot2.png', height=900))
    task3 = asyncio.create_task(async_generate_screenshot('my_page.html', 'async_screenshot3.png', device_scale_factor=3))

    # 等待所有任务完成
    results = await asyncio.gather(task1, task2, task3)

    print("\n所有截图任务已完成。")

if __name__ == "__main__":
    # 确保 my_page.html 和 another_page.html 在同一目录下
    asyncio.run(main())