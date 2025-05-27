from ..imports import *

def generate_color_palette(num_colors: int) -> List[str]:
    """
    生成系列十六进制颜色调色板

    `num_colors`: 生成颜色数量
    """
    # 随机选择一个基准色相（0-360度）
    base_hue = random.uniform(0, 360)
    
    colors = []
    for _ in range(num_colors):
        # 允许色相在±15度范围内波动（保持同色系）
        hue = (base_hue + random.uniform(-15, 15)) % 360
        # 饱和度控制（中等偏高，0.65-0.85）
        saturation = random.uniform(0.65, 0.85)
        # 亮度控制（避免过亮过暗，0.25-0.65）
        lightness = random.uniform(0.25, 0.65)
        # 将HSL转换为RGB（使用colorsys的hls转换）
        r, g, b = colorsys.hls_to_rgb(hue/360, lightness, saturation)
        # 转换为0-255整数值并确保范围正确
        r, g, b = [max(0, min(int(x * 255), 255)) for x in (r, g, b)]
        # 格式化为十六进制字符串
        hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        colors.append(hex_color)

    return colors

from pydantic import BaseModel
from typing import Type

def format_pydantic_config_markdown(config_model: BaseModel) -> str:
    """
    格式化 Pydantic 配置模型为 Markdown 列表格式。

    Args:
        config_model: Pydantic 配置模型类。
        indent_level: 当前缩进级别，用于处理嵌套模型。

    Returns:
        Markdown 格式的配置字符串。
    """
    markdown_output = ""

    # 添加模型描述
    if config_model.__doc__:
        markdown_output += f"## {config_model.__doc__.strip()}\n\n"

    # 遍历模型的字段
    for field_name, field in config_model.model_fields.items():
        default_value = field.default if field.default is not None else "无默认值"
        description = field.description if field.description else "无描述"

        markdown_output += f"- **{field_name} = {default_value}**: {description}\n"

        # 如果字段是嵌套的 Pydantic 模型，递归调用
        if isinstance(field.annotation, type) and issubclass(field.annotation, BaseModel):
            markdown_output += format_pydantic_config_markdown(field.annotation())
            markdown_output += "\n"

    return markdown_output