import subprocess
from pathlib import Path
from nonebot.log import logger

frontend_dir = Path(__file__).parent.parent / "external" / "html_render"

def check_npm_command() -> bool:
    """检查 npm 命令是否存在"""
    try:
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False


def verify_installation(directory: Path = frontend_dir) -> bool:
    """验证 npm 依赖是否安装成功 (简单检查 node_modules 目录)"""
    return (directory / "node_modules").is_dir()


def install_frontend_dependencies() -> bool:
    """安装渲染截图前端依赖"""
    logger.info("正在进行 ZikeQuote3 Node.js 依赖安装...")

    if not frontend_dir.is_dir():
        logger.error(f"无法找到目录 '{frontend_dir}'")
        return False

    if not check_npm_command():
        logger.error("找不到命令 'npm'")
        logger.error("请检查是否安装 Node.js 并加入系统环境变量")
        return False

    if verify_installation(frontend_dir):
        logger.info("Node.js 依赖已安装，跳过安装")
        return True

    try:
        subprocess.run(['npm', 'install'], check=True, cwd=frontend_dir)
        if verify_installation(frontend_dir):
            logger.info("Node.js 依赖安装成功。")
            return True
        else:
            logger.error("Node.js 依赖安装完成，但验证失败")
            return False
        
    except subprocess.CalledProcessError as e:
        logger.error(f"运行 'npm install' 时发生错误: {e}")
        logger.error(f"退出代码: {e.returncode}. 安装失败.")
        return False

    except Exception as e:
        logger.error(f"安装时发生错误: {e}")
        return False


if __name__ == "__main__":
    install_frontend_dependencies()